#
# Copyright 2020 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium
# is strictly prohibited.
#
"""Interact with an Anaml server using the REST API."""

from uuid import UUID
import requests
import base64
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging

from .checks import Check
from .cluster import Cluster
from .destination import Destination
from .feature import Feature, BareFeature, FeatureTemplate, GeneratedFeatures
from .merge_request import MergeRequest
from .model import FeatureStoreRun, FeatureSet, FeatureStore, Commit, Ref
from .table import Table
from . import version

__version__ = version.__version__

log = logging.getLogger(__name__)

__no_features = """No feature instances were generated for the following """
__no_features += """features:\n{the_features}.\n"""
__no_features += """This could be because the underlying dataset was empty, """
__no_features += """or because a predicate or window in the feature excluded"""
__no_features += """ all records in the dataset."""


class Anaml:
    """Anaml is a service class providing access to all functionality."""

    def __init__(self, url: str, apikey: str, secret: str, ref: Ref = None):
        """Create a new Anaml object.

        Access to the API requires a Personal Access Token which can be obtain on the users profile page
        on the web interface.

        Arguments:
            url: Base url for anaml server. e.g. https://anaml.company.com/api
            apikey: API key for Personal Access Token
            secret: API secret for Personal Access Token
            ref: optional BranchRef or CommitRef reference to act on
        """
        self._url = url
        self._token = base64.b64encode(bytes(apikey + ':' + secret, 'utf-8')).decode('utf-8')
        self._headers = {'Authorization': 'Basic ' + self._token}
        if ref is not None:
            self._ref = {ref.ref_type:  ref.ref}
        else:
            self._ref = {}

    def with_ref(self, new_ref: Ref):
        """Returns a new instance of Anaml that will act on the given `new_ref`.

        Args:
            new_ref: commit id or branch name

        Returns: Copy of Anaml with new ref
        """
        # This is a bit hacky
        new_anaml = Anaml(self._url, "", "", new_ref)
        new_anaml._token = self._token
        new_anaml._headers = self._headers

        return new_anaml

    def get(self, part):
        """Send a GET request to the Anaml server."""
        return requests.get(self._url + part, params=self._ref, headers=self._headers)

    def put(self, part, json):
        """Send a PUT request to the Anaml server."""
        return requests.put(self._url + part, params=self._ref, json=json, headers=self._headers)

    def post(self, part, json, **kwargs):
        """Send a POST request to the Anaml server."""
        return requests.post(self._url + part, params=self._ref, json=json, headers=self._headers, **kwargs)

    # Commits and Branches

    def get_current_commit(self, branch: str) -> Commit:
        """Get the current commit for a branch."""
        r = self.get(f"/branch/{branch}")
        result = self._json_or_handle_errors(r)
        return Commit.from_dict(result)

    # Cluster-related functions

    def get_clusters(self) -> list[Cluster]:
        """Get a list of all clusters defined (in the default branch) on the Anaml server."""
        r = self.get("/cluster")
        result = self._json_or_handle_errors(r)
        return [Cluster.from_dict(d) for d in result]

    def get_cluster(self, cluster_id: int) -> Cluster:
        """Get a clusters defined (in the default branch) on the Anaml server."""
        r = self.get(f"/cluster/{cluster_id}")
        result = self._json_or_handle_errors(r)
        return Cluster.from_dict(result)

    # Feature-related functions
    def get_features(self) -> list[BareFeature]:
        """Get a list of all features defined (in the default branch) on the Anaml server."""
        r = self.get("/feature")
        result = self._json_or_handle_errors(r)
        return [BareFeature.from_json(d) for d in result]

    def get_feature_templates(self) -> list[FeatureTemplate]:
        """Get a list of all features templates defined (in the default branch) on the Anaml server."""
        r = self.get("/feature-template")
        result = self._json_or_handle_errors(r)
        return [FeatureTemplate.from_json(d) for d in result]

    def get_feature(self, id: int) -> BareFeature:
        """Return the feature for the given `id`."""
        r = self.get("/feature/" + str(id))
        result = self._json_or_handle_errors(r)
        return BareFeature.from_json(result)

    def get_feature_template(self, id: int):
        """Return the feature template for the given `id`."""
        r = self.get("/feature-template/" + str(id))
        result = self._json_or_handle_errors(r)
        return FeatureTemplate.from_json(result)

    def get_generated_features(self, feature_store: str, primary_key: int) -> GeneratedFeatures:
        """Get the features generated from a feature store for a particular primary key value."""
        r = self.get("/generated-feature/" + feature_store + "/" + str(primary_key))
        result = self._json_or_handle_errors(r)
        return GeneratedFeatures.from_json(result)

    def create_feature(self, feature: Feature):
        """Create or update a feature definition on the Anaml server.

        If the feature object contains an ID, that feature will be updated;
        otherwise a new feature will be created.
        """
        endpoint = "/feature-template" if feature.isTemplate() else "/feature"

        if feature.get_id() is not None:
            r = self.put(endpoint + "/" + str(feature.get_id()),
                         json=feature.to_dict())
        else:
            r = self.post(endpoint, json=feature.to_dict())
            feature.set_id(int(r.text))

    def preview_feature(self, feature: Feature):
        """Show a matplotlib plot for the preview statistics of a feature.

        Arguments:
            feature: a Feature object
        """
        r = self.post("/feature-preview",
                      json={"features": [feature.to_dict()]})

        result = self._json_or_handle_errors(r)

        feature_stats = [fs
                         for pd in self.__to_list(result.get("previewData"))
                         for fss in self.__to_list(pd.get("featureStatistics"))
                         for fs in fss]
        [self._build_feature_plots(fs) for fs in feature_stats]
        self._warn_empty_feature_stats([fs.get("featureName") for
                                        fs in feature_stats
                                        if fs.get("adt_type") == "empty"])

    def sample_feature(self, feature: Feature):
        """Generate a sample of feature values.

        Arguments:
            feature: a Feature object

        Returns:
            a pandas dataframe of the feature sample values
        """
        r = self.post("/feature-sample",
                      json={"features": [feature.to_dict()]})

        result = self._json_or_handle_errors(r)
        return pd.DataFrame(result)

    def _build_feature_plots(self, fs):
        [self.__build_numerical_plots(qdata, fs.get("featureName"))
            for qdata in self.__to_list(fs.get("quantiles"))]
        [self.__build_categorical_plots(qdata, fs.get("featureName"))
            for qdata in self.__to_list(fs.get("categoryFrequencies"))]

    def _warn_empty_feature_stats(self, features: list[str]):
        if features:
            log.warning(__no_features.format(thefeatures=', '.join(features)))

    # Table-related functions
    def get_tables(self) -> list[Table]:
        """Retrieve all tables from the Anaml server."""
        r = self.get("/table")
        result = self._json_or_handle_errors(r)
        return [Table.from_dict(d) for d in result]

    def get_table(self, id: int) -> Table:
        """Retrieve a single table from the Anaml server."""
        r = self.get("/table/" + str(id))
        result = self._json_or_handle_errors(r)
        return Table.from_dict(result)

    # Destination-related functions
    def get_destinations(self) -> list[Destination]:
        """Get a list of all destinations from the Anaml server."""
        r = self.get("/destination")
        result = self._json_or_handle_errors(r)
        return [Destination.from_dict(d) for d in result]

    def get_destination(self, destination_id: int) -> Destination:
        """Get the details for a destination from the Anaml server."""
        r = self.get(f"/destination/{destination_id}")
        result = self._json_or_handle_errors(r)
        return Destination.from_dict(result)

    def get_feature_sets(self) -> list[FeatureSet]:
        """Get a list of feature sets from the Anaml server.."""
        r = self.get("/feature-set")
        result = self._json_or_handle_errors(r)
        return [
            FeatureSet.from_dict(r) for r in result
        ]

    def get_feature_set(self, featureSetId: int) -> FeatureSet:
        """Get the details for a feature set from the Anaml server."""
        r = self.get(f"/feature-set/{featureSetId}")
        result = self._json_or_handle_errors(r)
        return FeatureSet.from_dict(result)

    def get_feature_stores(self) -> list[FeatureStore]:
        """Get a list of all feature stores from the Anaml server."""
        r = self.get("/feature-store")
        result = self._json_or_handle_errors(r)
        return [
            FeatureStore.from_dict(r) for r in result
        ]

    def get_feature_store(self, feature_store_id: int) -> FeatureStore:
        """Get a feature stores from the Anaml server."""
        r = self.get(f"/feature-store/{feature_store_id}")
        result = self._json_or_handle_errors(r)
        return FeatureStore.from_dict(result)

    # Feature-store-released functions.

    def get_feature_store_runs(self, feature_store_id: int) -> list[FeatureStoreRun]:
        """Get a list of all runs of a given feature store from the Anaml server."""
        r = self.get(f"/feature-store/{feature_store_id}/run")
        result = self._json_or_handle_errors(r)
        return [FeatureStoreRun.from_dict(r) for r in result]

    def get_feature_store_run(self, feature_store_id: int, run_id: int) -> FeatureStoreRun:
        """Get the details for a feature store run from the Anaml server."""
        r = self.get(f"/feature-store/{feature_store_id}/run/{run_id}")
        result = self._json_or_handle_errors(r)
        return FeatureStoreRun.from_dict(result)

    # Merge Requests
    def get_merge_requests(self) -> list[MergeRequest]:
        """Get merge requests from the Anaml server."""
        r = self.get("/merge-request")
        result = self._json_or_handle_errors(r)
        return [
            MergeRequest.from_dict(r) for r in result
        ]

    def get_merge_request(self, id: str) -> list[MergeRequest]:
        """Get merge requests from the Anaml server."""
        r = self.get(f"/merge-request/{id}")
        result = self._json_or_handle_errors(r)
        return MergeRequest.from_dict(result)

    # Checks
    def get_checks(self, commit_id: UUID) -> list[Check]:
        """Get Checks for a commit from the Anaml server."""
        r = self.get(f"/checks/{commit_id}")
        result = self._json_or_handle_errors(r)
        return [
            Check.from_dict(r) for r in result
        ]

    def get_check(self, commit_id: UUID, check_id: int) -> Check:
        """Get a Check for a commit_id and check_id from the Anaml server."""
        r = self.get(f"/checks/{commit_id}/{check_id}")
        result = self._json_or_handle_errors(r)
        return Check.from_dict(result)

    def save_check(self, check: Check) -> Check:
        """Get Checks from the Anaml server."""
        if check.id is not None:
            self.put("/checks/" + str(check.commit) + "/" + str(check.id), json=check.to_json())
        else:
            result = self.post("/checks/" + str(check.commit), json=check.to_json())
            check_dict = check.to_dict()
            check_dict['id'] = int(result.content)
            check = Check(**check_dict)
        return check

    # Helpers
    @staticmethod
    def __build_numerical_plots(qdata, title):
        sns.set_style('whitegrid')
        plt.subplot(211)
        sns.kdeplot(x=np.array(qdata))
        plt.title(title)
        plt.subplot(212)
        sns.boxplot(x=np.array(qdata))
        plt.tight_layout()
        plt.show()

    @staticmethod
    def __build_categorical_plots(qdata, title):
        sns.set_style('whitegrid')
        sns.catplot(x="category", y="frequency", kind="bar",
                    data=pd.DataFrame(qdata))
        plt.title(title)
        plt.show()

    @staticmethod
    def __to_list(gotten):
        return [] if gotten is None else [gotten]

    @staticmethod
    def _warn_empty_stats(features: list[str]):
        if features:
            log.warning(__no_features.format(thefeatures=', '.join(features)))

    @staticmethod
    def _json_or_handle_errors(r):
        if r.ok:
            try:
                result = r.json()
                return result
            except json.JSONDecodeError:
                # Sorry, (no or invalid) JSON here
                log.error("No or invalid JSON received from server")
                log.error("Response content: " + r.content)
                r.raise_for_status()
        else:
            if "errors" in r:
                log.error(json.dumps(r.get("errors"), indent=4))

        r.raise_for_status()

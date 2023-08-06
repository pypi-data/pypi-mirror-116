# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021 The MVT Project Authors.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import glob
import os

import biplist

from mvt.common.utils import convert_timestamp_to_iso

from .base import IOSExtraction

WEBKIT_SESSION_RESOURCE_LOG_BACKUP_IDS = [
    "a500ee38053454a02e990957be8a251935e28d3f",
]

WEBKIT_SESSION_RESOURCE_LOG_ROOT_PATHS = [
    "private/var/mobile/Containers/Data/Application/*/SystemData/com.apple.SafariViewService/Library/WebKit/WebsiteData/full_browsing_session_resourceLog.plist",
    "private/var/mobile/Containers/Data/Application/*/Library/WebKit/WebsiteData/ResourceLoadStatistics/full_browsing_session_resourceLog.plist",
    "private/var/mobile/Library/WebClips/*/Storage/full_browsing_session_resourceLog.plist",
]

class WebkitSessionResourceLog(IOSExtraction):
    """This module extracts records from WebKit browsing session
    resource logs, and checks them against any provided list of
    suspicious domains."""

    def __init__(self, file_path=None, base_folder=None, output_folder=None,
                 fast_mode=False, log=None, results=[]):
        super().__init__(file_path=file_path, base_folder=base_folder,
                         output_folder=output_folder, fast_mode=fast_mode,
                         log=log, results=results)

    def _extract_browsing_stats(self, file_path):
        items = []

        file_plist = biplist.readPlist(file_path)
        if "browsingStatistics" not in file_plist:
            return items

        browsing_stats = file_plist["browsingStatistics"]

        for item in browsing_stats:
            items.append(dict(
                origin=item.get("PrevalentResourceOrigin", ""),
                redirect_source=item.get("topFrameUniqueRedirectsFrom", ""),
                redirect_destination=item.get("topFrameUniqueRedirectsTo", ""),
                subframe_under_origin=item.get("subframeUnderTopFrameOrigins", ""),
                subresource_under_origin=item.get("subresourceUnderTopFrameOrigins", ""),
                user_interaction=item.get("hadUserInteraction"),
                most_recent_interaction=convert_timestamp_to_iso(item["mostRecentUserInteraction"]),
                last_seen=convert_timestamp_to_iso(item["lastSeen"]),
            ))

        return items

    @staticmethod
    def _extract_domains(entries):
        if not entries:
            return []

        domains = []
        for entry in entries:
            if "origin" in entry:
                domains.append(entry["origin"])
            if "domain" in entry:
                domains.append(entry["domain"])

        return domains

    def check_indicators(self):
        if not self.indicators:
            return

        for key, entries in self.results.items():
            for entry in entries:
                source_domains = self._extract_domains(entry["redirect_source"])
                destination_domains = self._extract_domains(entry["redirect_destination"])

                # TODO: Currently not used.
                # subframe_origins = self._extract_domains(entry["subframe_under_origin"])
                # subresource_domains = self._extract_domains(entry["subresource_under_origin"])

                all_origins = set([entry["origin"]] + source_domains + destination_domains)

                if self.indicators.check_domains(all_origins):
                    self.detected.append(entry)

                    redirect_path = ""
                    if len(source_domains) > 0:
                        redirect_path += "SOURCE: "
                        for idx, item in enumerate(source_domains):
                            source_domains[idx] = f"\"{item}\""

                        redirect_path += ", ".join(source_domains)
                        redirect_path += " -> "

                    redirect_path += f"ORIGIN: \"{entry['origin']}\""

                    if len(destination_domains) > 0:
                        redirect_path += " -> "
                        redirect_path += "DESTINATION: "
                        for idx, item in enumerate(destination_domains):
                            destination_domains[idx] = f"\"{item}\""

                        redirect_path += ", ".join(destination_domains)

                    self.log.warning("Found HTTP redirect between suspicious domains: %s", redirect_path)

    def _find_paths(self, root_paths):
        results = {}
        for root_path in root_paths:
            for found_path in glob.glob(os.path.join(self.base_folder, root_path)):
                if not os.path.exists(found_path):
                    continue

                key = os.path.relpath(found_path, self.base_folder)
                if key not in results:
                    results[key] = []

        return results

    def run(self):
        self.results = {}

        try:
            self._find_ios_database(backup_ids=WEBKIT_SESSION_RESOURCE_LOG_BACKUP_IDS)
        except FileNotFoundError:
            pass
        else:
            if self.file_path:
                self.results[self.file_path] = self._extract_browsing_stats(self.file_path)
                return

        self.results = self._find_paths(root_paths=WEBKIT_SESSION_RESOURCE_LOG_ROOT_PATHS)
        for log_file in self.results.keys():
            self.log.info("Found Safari browsing session resource log at path: %s", log_file)
            self.results[log_file] = self._extract_browsing_stats(os.path.join(self.base_folder, log_file))

# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import
# pylint: disable=line-too-long, too-many-lines

helps['advisor'] = """
type: group
short-summary: Manage Azure Advisor.
"""

helps['advisor configuration'] = """
type: group
short-summary: Manage Azure Advisor configuration.
"""

helps['advisor configuration list'] = """
type: command
short-summary: List Azure Advisor configuration for the entire subscription.
"""

helps['advisor configuration show'] = """
type: command
short-summary: Show Azure Advisor configuration for the given subscription or resource group.
"""

helps['advisor configuration update'] = """
type: command
short-summary: Update Azure Advisor configuration.
examples:
  - name: Update low CPU threshold for a given subscription to 20%.
    text: >
        az advisor configuration update -l 20
  - name: Exclude a given resource group from recommendation generation.
    text: >
        az advisor configuration update -g myRG -e
  - name: Update Azure Advisor configuration. (autogenerated)
    text: az advisor configuration update --include --resource-group myRG
    crafted: true
"""

helps['advisor recommendation'] = """
type: group
short-summary: Review Azure Advisor recommendations.
"""

helps['advisor recommendation disable'] = """
type: command
short-summary: Disable Azure Advisor recommendations.
"""

helps['advisor recommendation enable'] = """
type: command
short-summary: Enable Azure Advisor recommendations.
examples:
  - name: Enable Azure Advisor recommendations. (autogenerated)
    text: az advisor recommendation enable --name MyRecommendation
    crafted: true
"""

helps['advisor recommendation list'] = """
type: command
short-summary: List Azure Advisor recommendations.
"""

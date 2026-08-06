# -*- coding: utf-8 -*-
DEFAULT_PROFILE = "profile-collective.volto.stickyblocks:default"


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile, run_dependencies)


def update_rolemap(context):
    update_profile(context, "rolemap")


def update_controlpanel(context):
    update_profile(context, "controlpanel")


def to_1001(context):
    update_rolemap(context)
    update_controlpanel(context)

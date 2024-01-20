init -990 python in mas_submod_utils:
    Submod(
        author="MayJay",
        name="MultiName",
        description="A submod that let's you save names to a list to switch between them easier, as well as adds a few other useful name-related options and a few topics. This submod utilizes the submod updater! Please open an issue on the repo, or go to my submod work server if there's an issue: https://discord.gg/Tx23rczN8N ",
        version="1.0.0",
        dependencies={},
        settings_pane=None,
        version_updates={}
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="MultiName",
            user_name="mayday-mayjay",
            repository_name="MJ-MAS-submod-multiname",
            submod_dir="/Submods/MultiName",
            extraction_depth=3,
            redirected_files=(
                "README.md"
            )
        )



SOURCES         = app2.py \
                  pyminer.py \
                  pmgui.py \
                  check_dependency.py \
                  features/base.py\


FORMS           = features/ui/base/aboutMe.ui \
                  features/ui/base/first_form.ui\
                  features/ui/base/option.ui \
                  features/ui/base/project_wizard.ui\
                  features/ui/base/pm_marketplace/main.ui\
                  features/ui/base/pm_marketplace/install.ui\
                  features/ui/base/pm_marketplace/uninstall.ui\
                  features/ui/base/pm_marketplace/package_manager_main.ui\

TRANSLATIONS    = languages/en/en.ts \
                  languages/zh_CN/zh_CN.ts \
                  languages/zh_TW/zh_TW.ts\

CODECFORTR      = UTF-8
CODECFORSRC     = UTF-8

# pylupdate5.exe pyminer.pro
# linguist.exe languages\en\en.ts languages\zh_CN\zh_CN.ts languages\zh_TW\zh_TW.ts
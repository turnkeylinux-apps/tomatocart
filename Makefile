COMMON_CONF = apache-credit

CREDIT_ANCHORTEXT = TomatoCart Appliance
CREDIT_LOCATION = ~ "^/(?!(.*admin|.*piwik))"

include $(FAB_PATH)/common/mk/turnkey/lamp.mk
include $(FAB_PATH)/common/mk/turnkey.mk

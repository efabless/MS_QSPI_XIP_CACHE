PLUSARGS += "+UVM_VERBOSITY=UVM_HIGH"
TOPLEVEL := top
MODULE   ?= top_module

AHB_FILES ?= $(PWD)/../../hdl/rtl/bus_wrappers/MS_QSPI_XIP_CACHE_ahbl.v
APB_FILES ?= ""
WB_FILES ?= ""
HDL_FILES ?= $(PWD)/../../hdl/rtl/MS_QSPI_XIP_CACHE.v
VIP_FILES ?= $(PWD)/../vip/sst26wf080b.v
VERILOG_SOURCES ?=  $(PWD)/top.v $(AHB_FILES) $(APB_FILES) $(WB_FILES) $(HDL_FILES) $(VIP_FILES)
RTL_MACROS += ""
BUS_TYPE ?= AHB
# ifeq ($(BUS_TYPE),APB)
#     RTL_MACROS += -DBUS_TYPE_APB
# else ifeq ($(BUS_TYPE),AHB)
#     RTL_MACROS += -DBUS_TYPE_AHB
# else ifeq ($(BUS_TYPE),WISHBONE)
#     RTL_MACROS += -DBUS_TYPE_WISHBONE
# endif
# RTL_MACROS ?= "-DSKIP_WAVE_DUMP"
YAML_FILE = $(PWD)/../../MS_QSPI_XIP_CACHE.yaml
MAKEFLAGS += --no-print-directory

# List of tests
TESTS := flashReadTest flashResetTest flashRdWrTest
# TESTS := flashResetTest

# Variable for tag - set this as required
SIM_TAG ?= default_tag

# Define SIM_PATH variable
SIM_PATH := $(PWD)/sim/$(SIM_TAG)

# Check and clone EF_UVM repository at the beginning of the Makefile execution

clone_ef_uvm := $(shell if [ ! -d "EF_UVM" ]; then \
	echo "Cloning the EF_UVM repository..."; \
	git clone https://github.com/efabless/EF_UVM.git; \
fi;)


include EF_UVM/Makefile.test

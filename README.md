# MS_QSPI_XIP_CACHE
Quad I/O SPI Flash memory controller with support for:
- AHB lite interface
- Execute in Place (XiP)
- Nx16 Direct-Mapped Cache (default: N=32).

Intended to be used with SoCs that have no on-chip flash memory. 


## Performance
The following data is obtained using Sky130 HD library
| Configuration | # of Cells (K) | Delay (ns) | I<sub>dyn</sub> (mA/MHz) | I<sub>s</sub> (nA) | 
|---------------|----------------|------------|--------------------------|--------------------|
| 16x16 | 7.2 | 12 | 0.0625 | 20 |
| 32x16 | 14.3 | 17  | 0.126 | 39.5 |


AHB-Lite Quad I/O SPI Flash memory controller with direct mapped cache and support for XiP.
## The wrapped IP


 The IP comes with an AHBL Wrapper

### Wrapped IP System Integration

```verilog
MS_QSPI_XIP_CACHE_APB INST (
        `TB_AHBL_SLAVE_CONN,
        .sck(sck)
        .ce_n(ce_n)
        .din(din)
        .dout(dout)
        .douten(douten)
);
```
> **_NOTE:_** `TB_APB_SLAVE_CONN is a convenient macro provided by [BusWrap](https://github.com/efabless/BusWrap/tree/main).

## Implementation example  

The following table is the result for implementing the MS_QSPI_XIP_CACHE IP with different wrappers using Sky130 PDK and [yosys](https://github.com/YosysHQ/yosys).
|Module | Number of cells | Max. freq |
|---|---|---|
|MS_QSPI_XIP_CACHE||  |
|MS_QSPI_XIP_CACHE_AHBL|||

### The Interface 


#### Ports 

|Port|Direction|Width|Description|
|---|---|---|---|
|sck|output|1|spi serial clock|
|ce_n|output|1|slave select signal|
|din|input|4|spi data in|
|dout|output|4|spi data out|
|douten|output|4|spi data out enable|

## Installation:
You can either clone repo or use [IPM](https://github.com/efabless/IPM) which is an open-source IPs Package Manager
* To clone repo:
```git clone https://https://github.com/shalan/MS_QSPI_FLASH_CTRL```
* To download via IPM , follow installation guides [here](https://github.com/efabless/IPM/blob/main/README.md) then run 
```ipm install MS_QSPI_XIP_CACHE```
### Run cocotb UVM Testbench:
In IP directory run:
 ```shell
 cd verify/uvm-python/
 ```
 ##### To run testbench for design with APB 
 To run all tests:
 ```shell
 make run_all_tests BUS_TYPE=APB
 ```
 To run a certain test:
 ```shell
 make run_<test_name> BUS_TYPE=APB
 ```
 To run all tests with a tag: 
 ```shell
 make run_all_tests TAG=<new_tag> BUS_TYPE=APB
 ```
 ##### To run testbench for design with APB
 To run all tests:
 ```shell
 make run_all_tests BUS_TYPE=AHB
 ```
 To run a certain test:
 ```shell
 make run_<test_name> BUS_TYPE=AHB
 ```
 To run all tests with a tag: 
 ```shell
 make run_all_tests TAG=<new_tag> BUS_TYPE=AHB
```

## Todo:
 - [ ] support for WB bus
 - [ ] Support cache configurations other than 16 bytes per line
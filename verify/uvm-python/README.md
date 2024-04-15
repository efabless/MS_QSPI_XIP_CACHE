# Verification notes

- only ahb is supoorted because wrapper is manually written
- To verify controller like this a vip(flash memory spi slave) is used to interact with controller spi interface
- Driver communication with the vip should be limited to reset the vip and load memory data into it. it should not drive the spi interface.
- Only read ahb commands are supported

[Tutorial followed](https://roboticsbackend.com/make-ros-launch-start-on-boot-with-robot_upstart/)

Commands to be run to get launch file running on pi on boot.

Should be in run src folder after a colcon build in the ws folder.

Warning need to install python packages with sudo.


```bash
ros2 run pi_main install 
```

```bash
sudo systemctl daemon-reload
```

### Adding udev Rules
This should automatically be done by the prior command `ros2 run pi_main install`. If not copy all the .rules files from `udev_rules` in this package to the `/etc/udev/rules.d` directory to use USB devices properly.

### For Testing without Rebooting
Runs in foreground for testing
```bash
sudo cwrubotix_pi-start
```

Runs in background
```bash
sudo systemctl start cwrubotix_pi.service
```
Kills in background
```bash
sudo systemctl stop cwrubotix_pi.service
```
### Unistall cwrubotix_pi
```bash
ros2 run robot_upstart uninstall cwrubotix_pi
```

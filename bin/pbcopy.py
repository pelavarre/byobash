7873856eb7b7    Brian Pan       Mon Apr 25 13:10:47 2022 -0700  PURE-254379: Bumped CCM to 3.2.9 (Save certificate components separately in CO KV store)
cfe07580d225    Jacob Melander  Mon Apr 25 13:10:42 2022 -0700  PURE-248320 Allow files to be renamed to a different case insensitive permutation of the same name
fde44a02da5c    Jacob Melander  Mon Apr 25 13:10:41 2022 -0700  PURE-250967 Disallow Rename/Move to case insensitive collisions when overwrite isn't allowed
95b5fb79eebc    Jacob Melander  Mon Apr 25 07:49:11 2022 -0700  PURE-254230 Workaround for Windows clients aborting DCERPC communication after successful bind
5a72b25779d3    Andrew Dumas    Fri Apr 22 15:07:24 2022 -0600  Revert "PURE-245380 Alerts should not be ignored by default"
cba0c19f47d4    Zijia Xie       Thu Apr 21 15:44:34 2022 -0700  PURE-241955 Increase chassis.list XML-RPC timeout
744354692288    Zijia Xie       Thu Apr 21 15:44:28 2022 -0700  PURE-253666 build.py has wrong ADD_IN_ETH_50G firmware
66771df11e3f    Yudan Wang      Thu Apr 21 07:45:04 2022 -0600  PURE-252326 Add retry to Windows attach_file_service to avoid flaky mount error
4d1b0ac2693a    Chu Zhang       Wed Apr 20 17:59:06 2022 -0700  PURE-249489 Warm NDU will lose pending actions on in memory Queue
7d7a8b4f9003    Hubert Chan     Wed Apr 20 17:59:00 2022 -0700  PURE-252041 Update REST 2.14 documentation
f9542ffd322b    Kevin Ko        Wed Apr 20 17:58:55 2022 -0700  PURE-253825 disable multipathd service with qemu-less builds
d0dcc75f159a    Andrew Dumas    Wed Apr 20 17:58:50 2022 -0700  PURE-245380 Alerts should not be ignored by default
429a6d348fcb    Zong Wang       Wed Apr 20 17:58:45 2022 -0700  PURE-254175 include pending replica-link in object_store check
691825ac1ce3    Renjie Fan      Wed Apr 20 17:58:38 2022 -0700  PURE-253036 Disable FPL.next in mergepool
fa71b1b78d85    Renjie Fan      Wed Apr 20 17:58:37 2022 -0700  PURE-252177 FPL profile for fresher NVR bics5 TLC drives
bc4ed6fe8d76    Renjie Fan      Wed Apr 20 17:58:36 2022 -0700  PURE-251462 Latency profile for Fresher NVR drive with B47R chips
21e52d2ca567    Renjie Fan      Wed Apr 20 17:58:35 2022 -0700  PURE-251495 FPL.Next latency profile for bics5 QLC drive
4df02eb8aafe    Renjie Fan      Wed Apr 20 17:58:34 2022 -0700  PURE-250062 Use tunable_sample of enable_fpl_next tunable
929a63fd95ef    Renjie Fan      Wed Apr 20 17:58:34 2022 -0700  PURE-249303 Enable FPL.Next on Oxygen
1fed49a4707c    Marten Heidemeyer       Wed Apr 20 12:14:34 2022 -0700  PURE-251564 SPBM and prepareToSnapshotVirtualVolume
31f5a52a907d    Jacob Hamilton  Wed Apr 20 12:14:29 2022 -0700  PURE-253303 storage leak of podman files preventing agent startup
816ab1001f33    Jacob Hamilton  Wed Apr 20 12:14:23 2022 -0700  PURE-253325 Revert optional bearer token expiration
30e011cd6972    Daniel Barton   Wed Apr 20 12:14:18 2022 -0700  PURE-252454 Change amount of rtfm workers on fan_out fasim version
6462397ceb37    Goutam Ghosh    Wed Apr 20 12:14:12 2022 -0700  PURE-252864 segment_reshape_mgr service startup took 17s
6e65f21e7751    Aset Dauletbaev Wed Apr 20 12:14:07 2022 -0700  PURE-253120 Use a random uint64_t for the next target ID
1e66f9143692    Jacob Hamilton  Wed Apr 20 12:14:02 2022 -0700  PURE-253256 grpc context abort does not stop execution as expected
3ee754ed7043    Charles Stephens        Wed Apr 20 12:13:57 2022 -0700  PURE-253489 Fix PXE path regression in ISO image
e209cfb2e283    Peter Mwesigwa  Tue Apr 19 17:41:06 2022 -0700  Revert "PURE-246252 Add MARVN2 to wssd production allowed list"
4813a3d18c8f    Peter Mwesigwa  Tue Apr 19 17:41:05 2022 -0700  Revert "PURE-245237 fw_update_tool support for MARVN2"
461ff4a063eb    Peter Mwesigwa  Tue Apr 19 17:41:05 2022 -0700  Revert "PURE-251851 Release wssd firmware 2.8.29"
bdf01432cc79    Rongjin Qiao    Tue Apr 19 17:40:58 2022 -0700  PURE-242198 Add BiCS5 4T/9T drives to the wssd whitelist
c5065fce8e71    Kevin Ko        Tue Apr 19 17:40:53 2022 -0700  PURE-253705 envoy podman init can fill up /var/tmp
61bcd5edabd9    Davis Duong     Tue Apr 19 17:40:47 2022 -0700  PURE-249865 Race in grabbing transactions lock after creating
69af206e673e    Caleb Gum       Tue Apr 19 12:17:14 2022 -0700  PURE-249700: cleanup user pods before testing readonly
1698530dc248    Caleb Gum       Tue Apr 19 12:17:08 2022 -0700  PURE-249465: Add rescan after test_array_with_no_connections_never_wins
d9ddc6ff9e9f    Zhijie Huang    Tue Apr 19 12:17:02 2022 -0700  PURE-252912 Stabalize test_file_gateway_repl_pod_check_snaps
67b08b4d3d70    Goutam Ghosh    Tue Apr 19 12:16:57 2022 -0700  PURE-253340 Use wide segments in rebalance group eviction unit test
7f332b598315    Vincent Wang    Tue Apr 19 12:16:52 2022 -0700  PURE-148958 Don't dump NVRAM sector buffers to logs on customer arrays
6f75aa10cf27    Bonnie Du       Tue Apr 19 12:16:46 2022 -0700  PURE-143833 add tunable to change 4 fabric cpus to 8
0b6f9d49685c    Hiram Zee       Tue Apr 19 12:16:40 2022 -0700  PURE-253903 - Update version string to 6.3.1 for 6.3.burgerking
a295841f8235    Drew Bernat     Mon Apr 18 10:14:57 2022 -0600  PURE-253125 - fix some NPIV NDU bugs
9a874c338e7d    Seamus Connor   Sat Apr 16 22:47:05 2022 -0700  PURE-253604 avoid leaking tpg_access_lock

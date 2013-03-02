# Bank Loader Plugin for Sublime Text 3 #


## Current Supported Hosts##

### kuaipan.com ###

- Implementation is simple, since target url is contained in _body_.

### dbank.com ###

- compatible with [dbank.js v2.8.3](http://st1.dbank.com/netdisk/js/custom-link1.js?v=2.8.3)
- main _decrypt_ component is ported from js.

### baidupan.com ###

- Simply as kuaipan.com

## User Guide ##

- Install:

``` shell
cd "~/Library/Application Support/Sublime Text 3/Packages"
git clone https://github.com/zyxar/bankloader Bankloader
cd Bankloader
git checkout sublime
```

- Usage:

	- default key binding: `Cmd+Ctrl+r`
	- automatically set input from paste board, and set back.
	- default download folder: `~/Desktop`
	



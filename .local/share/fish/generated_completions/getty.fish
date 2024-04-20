# getty
# Autogenerated from man page /usr/share/man/man8/getty.8.gz
complete -c getty -s 8 -l 8bits --description 'Assume that the tty is 8-bit clean, hence disable parity detection.'
complete -c getty -s a -l autologin --description 'Automatically log in the specified user without asking for a username or pass…'
complete -c getty -s c -l noreset --description 'Do not reset terminal cflags (control modes).'
complete -c getty -s E -l remote --description 'Typically the login(1) command is given a remote hostname when called by some…'
complete -c getty -l host -s h --description 'fakehost option and argument are added to the /bin/login command line.'
complete -c getty -l nohostname -s H --description 'is added to the /bin/login command line.'
complete -c getty -s f -l issue-file --description 'Display the contents of file instead of /etc/issue.'
complete -c getty -l flow-control --description 'Enable hardware (RTS/CTS) flow control.'
complete -c getty -s i -l noissue --description 'Do not display the contents of /etc/issue (or other) before writing the login…'
complete -c getty -s I -l init-string --description 'Set an initial string to be sent to the tty or modem before sending anything …'
complete -c getty -s J -l noclear --description 'Do not clear the screen before prompting for the login name.'
complete -c getty -s l -l login-program --description 'Invoke the specified login_program instead of /bin/login.'
complete -c getty -s L -l local-line --description 'Control the CLOCAL line flag.'
complete -c getty -s m -l extract-baud --description 'Try to extract the baud rate from the CONNECT status message produced by Haye…'
complete -c getty -l list-speeds --description 'Display supported baud rates.   These are determined at compilation time.'
complete -c getty -s n -l skip-login --description 'Do not prompt the user for a login name.'
complete -c getty -s N -l nonewline --description 'Do not print a newline before writing out /etc/issue.'
complete -c getty -s o -l login-options --description 'Options  and arguments that  are passed to login(1).'
complete -c getty -s p -l login-pause --description 'Wait for any key before dropping to the login prompt.'
complete -c getty -s r -l chroot --description 'Change root to the specified directory.'
complete -c getty -s R -l hangup --description 'Call vhangup() to do a virtual hangup of the specified terminal.'
complete -c getty -s s -l keep-baud --description 'Try to keep the existing baud rate.'
complete -c getty -s t -l timeout --description 'Terminate if no user name could be read within timeout seconds.'
complete -c getty -s U -l detect-case --description 'Turn on support for detecting an uppercase-only terminal.'
complete -c getty -s w -l wait-cr --description 'Wait for the user or the modem to send a carriage-return or a linefeed charac…'
complete -c getty -l nohints --description 'Do not print hints about Num, Caps and Scroll Locks.'
complete -c getty -l long-hostname --description 'By default the hostname is only printed until the first dot.'
complete -c getty -l erase-chars --description 'This option specifies additional characters that should be interpreted as a b…'
complete -c getty -l kill-chars --description 'This option specifies additional characters that should be interpreted as a k…'
complete -c getty -l chdir --description 'Change directory before the login.'
complete -c getty -l delay --description 'Sleep seconds before open tty.'
complete -c getty -l nice --description 'Run login with this priority.'
complete -c getty -l reload --description 'Ask all running agetty instances to reload and update their displayed prompts…'
complete -c getty -l version --description 'Display version information and exit.'
complete -c getty -l help --description 'Display help text and exit.'


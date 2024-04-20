# rngd
# Autogenerated from man page /usr/share/man/man8/rngd.8.gz
complete -c rngd -s b -l background --description 'Become a daemon (default).'
complete -c rngd -s f -l foreground --description 'Do not fork, nor detach from the controlling terminal.'
complete -c rngd -s R -l rng-driver --description 'Entropy source driver.'
complete -c rngd -s o -l random-device --description 'Kernel device used for entropy output.'
complete -c rngd -s r -l rng-device --description 'Kernel device, fifo or file used for entropy input by the stream entropy sour…'
complete -c rngd -l hrng --description 'Selects known-good defaults for some HRNGs.   help lists all known HRNGs.'
complete -c rngd -s H -l rng-entropy --description 'Entropy per bit of input data.'
complete -c rngd -s Q -l rng-quality --description 'Selects the quality of the random data an entropy source will generate.'
complete -c rngd -s B -l rng-buffers --description 'Number of 20000 bit buffers to use.'
complete -c rngd -s s -l random-step --description 'Number of bytes written to random-device at a time.'
complete -c rngd -s W -l fill-watermark --description 'Once we start doing it, feed entropy to random-device until at least fill-wat…'
complete -c rngd -s t -l feed-interval --description 'If feed-interval is not zero, rngd will force-feed entropy to the random devi…'
complete -c rngd -l timeout --description 'Deprecated, use --feed-interval instead.'
complete -c rngd -s T -l rng-timeout --description 'Time to wait for data to start coming from the entropy source, before giving …'
complete -c rngd -s p -l pidfile --description 'File to write PID to when running in background mode.'
complete -c rngd -s '?' -l help --description 'Give a short summary of all program options.'
complete -c rngd -s V -l version --description 'Print program version.'


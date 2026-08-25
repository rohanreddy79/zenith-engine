# sqrl crash demo — renders README's hero GIF.
#
# Requires charmbracelet/vhs (https://github.com/charmbracelet/vhs):
#   vhs docs/marketing/demo.tape
# then commit the result as docs/assets/demo.gif and swap it into the
# README's "See it survive" section.

Output docs/assets/demo.gif
Set FontSize 15
Set Width 940
Set Height 560
Set Padding 16
Set TypingSpeed 40ms

Hide
Type "cargo build --release -p crash_me 2>/dev/null"
Enter
Sleep 3s
Type "clear"
Enter
Show

Type "cargo run --release -p crash_me"
Enter
Sleep 8s

#! /bin/sh
# https://adventofcode.com/2020/day/8

#set -x

input_file=$1
max_line=$(wc -l $1 | awk '{print $1}')
tempfile=$(mktemp)
changelog=$(mktemp)

cleanup () {
    rm $tempfile
    rm $changelog
}
trap cleanup EXIT

is_line_valid () {
    [ $line -lt 1 ] && return 1
    [ $line -gt $max_line ] && return 2
    [ $line -eq $max_line ] && jackpot
    [ $(grep -cFx $line $tempfile) -gt 0 ] && return 3
    return 0
}

should_we_change () {
    [ $did_change -gt 0 ] && return 1
    [ "$instruction" = "acc" ] && return 2
    [ $(grep -cFx $line $changelog) -gt 0 ] && return 3
    return 0
}

jackpot () {
    process_line $(get_line $max_line)
    echo $accumulator
    exit
}

get_line () {
    sed -ne "$line p" $input_file
}

process_line () {
    instruction=$1
    if should_we_change; then
	[ "$instruction" = "nop" ] && instruction="jmp" || instruction="nop"
	echo $line >>$changelog
	did_change=1
    fi
    case $instruction in
	jmp)
	    line=$(( line + $2 ))
	    return;;
	acc)
	    accumulator=$(( accumulator + $2 ));;
    esac
    line=$(( line + 1 ))
}

cnt_nops=$(grep -cF 'nop' $1)
cnt_jmps=$(grep -cF 'jmp' $1)
max_change=$(( cnt_nops + cnt_jmps))
i=0
while [ $i -lt $max_change ]; do
    echo >$tempfile
    line=1
    accumulator=0
    did_change=0
    i=$(( i + 1 ))
    while is_line_valid; do
      echo $line >>$tempfile
      process_line $(get_line)
    done
done

echo "We have failed."

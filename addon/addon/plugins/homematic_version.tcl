#!/bin/tclsh
#

load tclrega.so
load tclrpc.so


set result [catch {exec curl -s https://raspberrymatic.de/LATEST-VERSION.js} verstring]
set result [regexp {homematic\.com\.setLatestVersion\('(.+)', 'HM-RASPBERRYMATIC'\);} $verstring match latest ]
set result [catch {exec grep PLATFORM /VERSION | cut -d= -f2} platform]
set result [catch {exec grep VERSION /VERSION | cut -d= -f2} currentversion]


#if { $currentversion eq $latest } {
#  puts { "RaspberryMatic version: $currentversion (up to date)" }
#} else {
#  puts { "RaspberryMatic version: $currentversion ($latest is available)" }
#}

puts "<<<homematic_version:sep(59)>>>"
puts "VERSION_INFO;homematic_version;$currentversion;$latest"
#exec echo "Current: " $currentversion >> /tmp/updatecheck
#exec echo "Latest:  " $latest         >> /tmp/updatecheck





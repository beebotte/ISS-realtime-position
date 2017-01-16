ISS Realtime Position
=====================

This package contains two source files:
 * iss_position_pub.py: computes the position of the International Space Station from [Two Line Element](http://en.wikipedia.org/wiki/Two-line_element_set) data published by [CelesTrak](http://www.celestrak.com/NORAD/elements/stations.txt) and publishes it to Beebotte every second. You need to update the file with a valid channel token or with your account's ACCESS and SECRET keys.
 * iss.html: a simple HTML + JavaScript page that subscribes to ISS data published on Beebotte to display the ISS position on Google Maps.

Check this [tutorial](http://beebotte.com/tutorials/iss_realtime_position) for details and this [live demo](http://beebotte.com/iss.html) to see it in action!

## Author
[Bachar Wehbi](http://twitter.com/bachwehbi)

## License
Copyright 2013 - 2017 Beebotte.

[The MIT License](http://opensource.org/licenses/MIT)

# gerrit-webhook

gerrit-webhook is a [Gerrit](http://code.google.com/p/gerrit/) `change-merged`
hook script that posts JSON data to a webhook capable server.

This implements the [GitHub](http://github.com) [Web hooks
API](http://github.com/guides/post-receive-hooks) pretty closely, but differs
a little since this is triggered by merged reviews, not ref updates.

This script was originally written for the purpose of
[Sprint.ly](http://sprint.ly) integration and allows arbitrary Gerrit instances
to use webhook capable services.

## Usage

To use gerrit-webhook, just copy `changed-merged.py` to your
Gerrit instance's `hooks` dir and call it `change-merged`. Be sure to
set it executable with `chmod 755 change-merged` as well.

### Configuration

Sample configuration information is listed at the top of the
`change-merged.py` script, that you will want to change for your environment.

# License

Copyright (c) 2012, JT Olds <hello@jtolds.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import ctypes, os, sys
libcef_so = os.path.join(os.path.dirname(os.path.abspath(__file__)),\
        'libcef.so')
if os.path.exists(libcef_so):
    # Import local module
    ctypes.CDLL(libcef_so, ctypes.RTLD_GLOBAL)
    if 0x02070000 <= sys.hexversion < 0x03000000:
        import cefpython_py27 as cefpython
    else:
        raise Exception("Unsupported python version: %s" % sys.version)
else:
    # Import from package
    from cefpython3 import cefpython

import gobject


Embedded_Browser_Initialized = False

def create_embedded_browser(parent_control, start_url):
    class Embedded_Browser(object):
        @staticmethod
        def _find_ctrl_id(ctrl):
            import re
            ctrl_type = ctrl.__class__.__name__
            hexID = re.search(ctrl_type + " at 0x(\w+)", str(ctrl)).group(1)
            return int(hexID, 16)

        def __init__(self, parent_control, start_url):
            windowID = Embedded_Browser._find_ctrl_id(parent_control)
            windowInfo = cefpython.WindowInfo()
            windowInfo.SetAsChild(windowID)

            self.browser = cefpython.CreateBrowserSync(
                windowInfo,
                browserSettings={},
                navigateUrl=start_url)

            gobject.timeout_add(10, self._on_timer)
            # TODO: It may be a better idea to look for a page onLoad
            gobject.timeout_add(1000, self._hack_crosshair)
            
        def _hack_crosshair(self):
            """ Show a crosshair in the middle of the page """
            hack = "" + \
                   "var img = document.createElement('img');" + \
                   "img.src = 'http://www.clker.com/cliparts/v/Z/s/J/Y/y/crosshair-md.png';" + \
                   "img.style.position='absolute';" + \
                   "img.style.left='50%';" + \
                   "img.style.marginLeft='-150px';" + \
                   "img.style.top='50%';" + \
                   "img.style.marginTop='-150px';" + \
                   "document.body.appendChild(img);" 
            self.browser.GetMainFrame().ExecuteJavascript(hack)
            # Tell gobject we don't need to trigger this callback again
            return False

        def _on_timer(self):
            cefpython.MessageLoopWork()
            return True

        def get_url(self):
            return self.browser.GetUrl()

    if not Embedded_Browser_Initialized:
        settings = {
            "debug": False,
            "log_severity": cefpython.LOGSEVERITY_INFO,
            "log_file": "", # Disabled
            # This directories must be set on Linux
            "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
            "resources_dir_path": cefpython.GetModuleDirectory(),
            "browser_subprocess_path": "%s/%s" % (cefpython.GetModuleDirectory(), "subprocess"),
        }

        cefpython.Initialize(settings)
        gobject.threads_init()
        import atexit
        atexit.register(cefpython.Shutdown)

    return Embedded_Browser(parent_control, start_url)


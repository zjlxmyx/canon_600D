import CanonLib

c = CanonLib.CanonCamera()
err = c.Init_Camera()
if err is not None:
    print(err)
err = c.set_LiveView_ready()
if err is not None:
    print(err)
err = c.get_Live_image()
if err is not None:
    print(err)

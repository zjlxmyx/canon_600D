import CanonLib

c = CanonLib.CanonCamera()
err = c.Init_Camera()
if type(err) is str:
    print(err)
err = c.set_LiveView_ready()
if type(err) is str:
    print(err)
err = c.get_Live_image()
if type(err) is str:
    print(err)

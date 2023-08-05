
def read_ellipses_from_csv(dataframe, scale=1., ellipse_scale=1.):
    ellipses = []
    for _, ellipse in dataframe.iterrows():
        ellipse_info = read_ellipse_from_row(ellipse, scale=scale, ellipse_scale=ellipse_scale)
        ellipses.append(ellipse_info)
    return ellipses


def read_ellipse_from_row(row, scale=1., ellipse_scale=1.):
    angle = 180 - row.Angle
    position = (row.X*scale, row.Y*scale)
    size = (row.Major*scale*ellipse_scale, row.Minor*scale*ellipse_scale)
    ellipse_info = (position, size, angle)
    return ellipse_info

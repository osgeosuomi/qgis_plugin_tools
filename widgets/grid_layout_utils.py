from qgis.PyQt.QtWidgets import QGridLayout, QLayoutItem

__copyright__ = "Copyright 2020-2021, Gispo Ltd, 2026 OSGeo Suomi"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

""" Removing functionality adapted from C example
https://stackoverflow.com/a/19256990/10068922 """


def remove_row(layout: QGridLayout, row: int, delete_widgets: bool = True) -> None:
    """
    Removes the contents of the given layout row.

    :param layout:
    :param row:
    :param delete_widgets:
    :return:
    """
    _remove(layout, row, -1, delete_widgets)
    layout.setRowMinimumHeight(row, 0)
    layout.setRowStretch(row, 0)


def remove_column(
    layout: QGridLayout, column: int, delete_widgets: bool = True
) -> None:
    """
    Removes the contents of the given layout column.

    :param layout:
    :param column:
    :param delete_widgets:
    :return:
    """
    _remove(layout, -1, column, delete_widgets)
    layout.setColumnMinimumWidth(column, 0)
    layout.setColumnStretch(column, 0)


def remove_cell(
    layout: QGridLayout, row: int, column: int, delete_widgets: bool = True
) -> None:
    """
    Removes the contents of the given layout cell.

    :param layout:
    :param row:
    :param column:
    :param delete_widgets:
    :return:
    """
    _remove(layout, row, column, delete_widgets)


def _remove(layout: QGridLayout, row: int, column: int, delete_widgets: bool) -> None:
    for i in reversed(range(1, layout.count())):
        r, c, rs, cs = layout.getItemPosition(i)
        if (row == -1 or (r <= row < r + rs)) and (
            column == -1 or (c <= column < c + cs)
        ):
            item: QLayoutItem = layout.takeAt(i)

            layout.removeItem(item)
            widget = item.widget()
            if widget is not None:
                layout.removeWidget(widget)
                widget = None
            if delete_widgets:
                _delete_child_widgets(item)
            del item


def _delete_child_widgets(item: QLayoutItem) -> None:
    """
    Deletes all child widgets of the given layout item.

    :param item:
    :return:
    """
    layout = item.layout()
    if layout:
        for i in range(layout.count()):
            _delete_child_widgets(layout.itemAt(i))
        layout.deleteLater()
    widget = item.widget()
    if widget is not None:
        widget.hide()
        # noinspection PyTypeChecker
        widget.setParent(None)
        widget = None
    del item
    item = None  # noqa: F841

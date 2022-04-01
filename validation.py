from PySide6.QtWidgets import QTextEdit

from randoconfig import ConfigurationCheckResult


def show_validation_result(view: QTextEdit, results: [ConfigurationCheckResult]):
    lines = ['<pre style="font-size: 14px">']
    for result in results:
        lines.append('{}'.format(result.name))
        for info in result.infos:
            lines.append('<span style="color: #00e600">\u2714</span> {}'.format(info))
        for error in result.errors:
            lines.append('<span style="color: #ffb4a9">\u2718</span> {}'.format(error))
        lines.append('')
    lines.append('</pre>')
    view.setHtml('\n'.join(lines))

from ancv.data.models.resume import ResumeSchema
from ancv.visualization import WIDTH, Template
from ancv.visualization.templates import BerlinBasic
from rich.console import Console


def render(resume: ResumeSchema, template: type[Template] = BerlinBasic) -> str:
    console = Console(
        width=WIDTH,
        color_system="256",
        force_terminal=False,
        force_jupyter=False,
        force_interactive=False,
        no_color=False,
        tab_size=4,
        legacy_windows=False,
    )

    with console.capture() as capture:
        console.print(template(resume))

    return capture.get()

from operator import attrgetter

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty

from .FuncionesArchivos import ObtenerValor, SalvarValor, ObtenerArchivo
from .extras import mostrarMensajeBox
from .funcionesExtras import asignarDinámica, cargarFuente


class superindice(bpy.types.Operator):
    bl_idname = "scene.superindice"
    bl_label = "Generdor Indices"
    bl_description = "Agrega Markas como Texto en el video"
    bl_options = {"REGISTER", "UNDO"}

    Duracion: FloatProperty(name="duracion", description="duracion indice", default=1, min=0)

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):

        indices = context.scene.timeline_markers
        scene = context.scene
        seq = scene.sequence_editor
        render = context.scene.render
        framerate = render.fps / render.fps_base

        if hasattr(seq, "strips_all"):
            secuencias = list(seq.strips_all)
            colección_secuencias = seq.strips
        elif hasattr(seq, "sequences_all"):
            secuencias = list(seq.sequences_all)
            colección_secuencias = seq.sequences
        else:
            secuencias = []
            colección_secuencias = None

        if indices is None:
            return {"CANCELLED"}
        indices = sorted(indices, key=attrgetter("frame"))
        indices = indices[1:]

        dataIndice = ObtenerArchivo("data/indice.json")

        if dataIndice is None:
            self.report({"INFO"}, f"No informacion de animacion .config/pluginBlenderChepeCarlos/data/indice.json")
            mostrarMensajeBox("No informacion de animacion .config/pluginBlenderChepeCarlos/data/indice.json", title="Error", icon="ERROR")

            return {"FINISHED"}

        dataIndiceExtra = ObtenerArchivo("data/indice_extra.json")

        if dataIndiceExtra is None:
            self.report({"INFO"}, f"No informacion de animacion .config/pluginBlenderChepeCarlos/data/indice_extra.json")
            mostrarMensajeBox("No informacion de animacion .config/pluginBlenderChepeCarlos/data/indice_extra.json", title="Error", icon="ERROR")

            return {"FINISHED"}

        fuente = dataIndiceExtra.get("fuente", None)
        tiempoDesaparecer = dataIndiceExtra.get("tiempo_desaparecer", 0.5)
        animaciónDesaparecer = dataIndiceExtra.get("animacion_desaparecer", "OUT")

        prefijo = "indice."

        for secuencia in secuencias:
            Titulo = secuencia.name
            if Titulo.startswith(prefijo) and colección_secuencias is not None:
                self.report({"INFO"}, f"borrar[{Titulo}]")
                colección_secuencias.remove(secuencia)

        duraciónIndice = int(dataIndiceExtra.get("duracion", 5) * framerate)
        canal = int(dataIndiceExtra.get("canal", 8))

        for indice in indices:
            Titulo = indice.name
            if not Titulo.startswith(">"):
                frame = indice.frame
                frameInicio = int(frame)
                frameFin = int(frame + duraciónIndice)
                duracion = max(1, frameFin - frameInicio)

                clipActual = self.agregarTexto(context, colección_secuencias, frameInicio, frameFin, duracion, canal)
                if clipActual is None:
                    self.report({"ERROR"}, f"No se pudo crear strip para: {Titulo}")
                    continue
                clipActual.name = f"{prefijo}{Titulo}"
                clipActual.text = Titulo

                if fuente is not None:
                    try:
                        idFuenteSelection, idFuente = cargarFuente(fuente)
                        clipActual.font = bpy.data.fonts[idFuenteSelection]
                    except FileNotFoundError:
                        mostrarMensajeBox(
                            f"No se encontró la fuente:\n{fuente}\n\nRevisa 'fuente' en data/indice_extra.json",
                            title="Error de Fuente",
                            icon="ERROR",
                        )
                        self.report({"ERROR"}, f"Fuente no encontrada: {fuente}")
                        return {"FINISHED"}

                clipActual.color_tag = "COLOR_06"

                for propiedad, valor in dataIndice.items():
                    self.report({"INFO"}, f"probando[{propiedad}] {valor}")
                    if propiedad is None:
                        continue
                    if valor is not None:
                        if asignarDinámica(clipActual, propiedad, valor):
                            self.report({"INFO"}, f"Asignar[{propiedad}] {valor}")

                try:
                    bpy.ops.sequencer.fades_add(duration_seconds=tiempoDesaparecer, type=animaciónDesaparecer)
                except Exception as error:
                    self.report({"WARNING"}, f"No se pudo agregar fade: {error}")

        return {"FINISHED"}

    def agregarTexto(self, context, colección, frameInicio, frameFin, duracion, canal):
        nombreTemporal = f"indice.tmp.{canal}.{frameInicio}"
        try:
            return colección.new_effect(
                name=nombreTemporal,
                type="TEXT",
                channel=canal,
                frame_start=frameInicio,
                frame_end=frameFin,
            )
        except TypeError:
            try:
                return colección.new_effect(
                    name=nombreTemporal,
                    type="TEXT",
                    channel=canal,
                    frame_start=frameInicio,
                    length=duracion,
                )
            except TypeError:
                try:
                    return colección.new_effect(nombreTemporal, "TEXT", canal, frameInicio, frameFin)
                except Exception as error:
                    self.report({"ERROR"}, f"Error creando strip: {error}")
                    return None
        except Exception as error:
            self.report({"ERROR"}, f"Error creando strip: {error}")
            return None

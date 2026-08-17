**Component Layer:**



*Raw diagram stored in:*

**\[RAW\_DIAGRAM\_PATH]**



*Review the example component layer stored in:*

**\[EXAMPLE\_COMPONENT\_LAYER\_PATH]**



*Store the resulting diagram in:*

**\[OUTPUT\_DIAGRAM\_PATH]**



*Store all your artifacts and code in:*

**\[WORKING\_FOLDER\_PATH]**



*In the example component layer, the components are detected with orange bounding boxes, while the busbars are detected with dark green bounding boxes.*



*For the raw diagram, create a similar component layer using bounding boxes, following the example layer as closely as possible. Use orange bounding boxes for components and dark green bounding boxes for busbars.*



*Detect and bound the visible components and busbars in the raw diagram. Use the example component layer as the primary reference for determining what should be classified as a component or busbar and how the bounding boxes should be positioned.*



*Warning: Do not use any off-the-shelf OCR libraries, such as TesseractOCR or RapidOCR. Instead, use the visual understanding capabilities of the GPT-5.5 model to inspect the diagram and produce the component layer. Zoom into and crop relevant regions of the diagram as required to accurately identify the components and busbars.*



*Preserve the original raw diagram and overlay only the required bounding boxes to produce the final component layer.*







**Wire Layer:**



*Raw diagram stored in:*

**\[RAW\_DIAGRAM\_PATH]**



*Review the example wire layer stored in:*

**\[EXAMPLE\_WIRE\_LAYER\_PATH]**



*Store the resulting diagram in:*

**\[OUTPUT\_DIAGRAM\_PATH]**



*Store all your artifacts and code in:*

**\[WORKING\_FOLDER\_PATH]**



*In the example wire layer, the wires are traced with red lines.*



*For the raw diagram, create a similar wire layer using wire tracing, following the example layer as closely as possible.*



*Detect the valid wire connections and mark them using red lines. Use the example wire layer as the primary reference for determining what should be classified as a wire and how it needs to be marked.*



*Warning: Do not use any off-the-shelf OCR libraries, such as TesseractOCR or RapidOCR. Instead, use the visual understanding capabilities of the GPT-5.5 model to inspect the diagram and produce the wire layer. Zoom into and crop relevant regions of the diagram as required to accurately identify the wires and their connections.*



*Preserve the original raw diagram and overlay only the required red wire tracings to produce the final wire layer.*







**Text Layer:**



*Raw diagram stored in:*

**\[RAW\_DIAGRAM\_PATH]**



*Review the example text layer stored in:*

**\[EXAMPLE\_TEXT\_LAYER\_PATH]**



*Store the resulting diagram in:*

**\[OUTPUT\_DIAGRAM\_PATH]**



*Store all your artifacts and code in:*

**\[WORKING\_FOLDER\_PATH]**



*In the example text layer, the detected text is marked with blue bounding boxes.*



*For the raw diagram, create a similar text layer using bounding boxes, following the example layer as closely as possible.*



*Detect the valid text elements in the raw diagram and mark them using blue bounding boxes. Use the example text layer as the primary reference for determining what should be classified as text and how the bounding boxes should be positioned. The bounding boxes should closely enclose the corresponding text without unnecessarily covering surrounding diagram elements.*



*Warning: Do not use any off-the-shelf OCR libraries, such as TesseractOCR or RapidOCR. Instead, use the visual understanding capabilities of the GPT-5.5 model to inspect the diagram and produce the text layer. Zoom into and crop relevant regions of the diagram as required to accurately identify the text elements.*



*Preserve the original raw diagram and overlay only the required blue bounding boxes to produce the final text layer.*





**Junction/Node Layer:** 



*Raw diagram stored in:*

**\[RAW\_DIAGRAM\_PATH]**



*Review the example junction/node layer stored in:*

**\[EXAMPLE\_JUNCTION\_NODE\_LAYER\_PATH]**



*Store the resulting diagram in:*

**\[OUTPUT\_DIAGRAM\_PATH]**



*Store all your artifacts and code in:*

**\[WORKING\_FOLDER\_PATH]**



*In the example junction/node layer, the wire topology nodes are marked using colored points based on their type:*



*Endpoints are marked with dark blue points.*

*T-junctions are marked with orange points.*

*Junctions are marked with purple points.*



*For the raw diagram, create a similar junction/node layer, following the example layer as closely as possible.*



*Detect the valid wire topology nodes and mark them using the corresponding colored points. Use the example junction/node layer as the primary reference for determining what should be classified as an endpoint, T-junction, or junction, as well as where and how each point should be positioned.*



*Place each point precisely at the corresponding wire connection or termination location, following the positioning and visual conventions shown in the example layer.*



*Warning: Do not use any off-the-shelf OCR libraries, such as TesseractOCR or RapidOCR. Instead, use the visual understanding capabilities of the GPT-5.5 model to inspect the diagram and produce the junction/node layer. Zoom into and crop relevant regions of the diagram as required to accurately identify the wire topology and its nodes.*



*Preserve the original raw diagram and overlay only the required colored node markers to produce the final junction/node layer.*


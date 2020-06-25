from HyperGuiModules import *
import logging

logging.basicConfig(level=logging.DEBUG)


def main():
    (window, introduction, input_output, image_diagram, hist_calculation, spec_calculation) = init()

    listener = ModuleListener()

    # introduction
    Introduction(introduction)

    # histogram calculation
    HistCalculation(hist_calculation, listener)

    # histogram calculation
    SpecCalculation(spec_calculation, listener)

    # analysis and form
    analysis_and_form_frame = frame(input_output, BACKGROUND, 1, 0, 4, 2)
    analysis_and_form_module = AnalysisAndForm(analysis_and_form_frame, listener)
    listener.attach_module(ANALYSIS_AND_FORM, analysis_and_form_module)

    # source and output
    source_and_output_frame = frame(input_output, BACKGROUND, 0, 0, 1, 2)
    source_and_output_module = SourceAndOutput(source_and_output_frame, listener)
    listener.attach_module(SOURCE_AND_OUTPUT, source_and_output_module)

    # save
    save_frame = frame(input_output, BACKGROUND, 5, 0, 1, 1)
    save_module = Save(save_frame, listener)
    listener.attach_module(SAVE, save_module)

    # save csvs
    csv_frame = frame(input_output, BACKGROUND, 0, 2, 6, 1)
    csv_module = CSVSaver(csv_frame, listener)
    listener.attach_module(CSV, csv_module)

    # info
    info_frame = frame(input_output, BACKGROUND, 5, 1, 1, 1)
    info_module = Info(info_frame, listener)
    listener.attach_module(INFO, info_module)

    # parameter specification
    parameter_frame = frame(input_output, BACKGROUND, 0, 3, 2, 1)
    parameter_module = Parameter(parameter_frame, listener)
    listener.attach_module(PARAMETER, parameter_module)

    # original colour
    og_color_frame = frame(image_diagram, BACKGROUND, 0, 0, 7, 6)
    og_color_module = OGColour(og_color_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR, og_color_module)

    # original colour data
    og_color_data_frame = frame(image_diagram, BACKGROUND, 2, 12, 3, 2)
    og_color_data_module = OGColourData(og_color_data_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR_DATA, og_color_data_module)

    # recreated colour
    recreated_color_frame = frame(image_diagram, BACKGROUND, 7, 0, 7, 3)
    recreated_color_module = RecColour(recreated_color_frame, listener)
    listener.attach_module(RECREATED_COLOUR, recreated_color_module)

    # recreated colour data
    rec_color_data_frame = frame(image_diagram, BACKGROUND, 5, 12, 4, 2)
    rec_color_data_module = RecreatedColourData(rec_color_data_frame, listener)
    listener.attach_module(RECREATED_COLOUR_DATA, rec_color_data_module)

    # new colour
    new_color_frame = frame(image_diagram, BACKGROUND, 7, 3, 7, 3)
    new_color_module = NewColour(new_color_frame, listener)
    listener.attach_module(NEW_COLOUR, new_color_module)

    # new colour data
    new_color_data_frame = frame(image_diagram, BACKGROUND, 9, 12, 3, 2)
    new_color_data_module = NewColourData(new_color_data_frame, listener)
    listener.attach_module(NEW_COLOUR_DATA, new_color_data_module)

    # diagram
    diagram_frame = frame(image_diagram, BACKGROUND, 0, 12, 2, 2)
    diagram_module = Diagram(diagram_frame, listener)
    listener.attach_module(DIAGRAM, diagram_module)

    # histogram
    histogram_frame = frame(image_diagram, BACKGROUND, 0, 6, 8, 6)
    histogram_module = Histogram(histogram_frame, listener)
    listener.attach_module(HISTOGRAM, histogram_module)

    # absorption
    absorption_spec_frame = frame(image_diagram, BACKGROUND, 8, 6, 6, 6)
    absorption_module = AbsorptionSpec(absorption_spec_frame, listener)
    listener.attach_module(ABSORPTION_SPEC, absorption_module)

    # colourbar
    colour_frame = frame(image_diagram, BACKGROUND, 12, 12, 2, 2)
    colour_module = Colour(colour_frame, listener)

    window.mainloop()


if __name__ == '__main__':
    main()

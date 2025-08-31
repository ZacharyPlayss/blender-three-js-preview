export function createPositionSliders(gui, element, sliderStart, sliderEnd,step = 1) {
    if(element.position == null) {
        throw new Error("The given element does not have a position attribute.");
    }
    const folder = gui.addFolder(element.name + " position" || 'Position');
    folder.add(element.position, 'x', sliderStart, sliderEnd,step);
    folder.add(element.position, 'y', sliderStart, sliderEnd,step);
    folder.add(element.position, 'z', sliderStart, sliderEnd,step);
    folder.close();
}

export function createRotationSliders(gui, element, sliderStart, sliderEnd, step = 1) {
    if(element.rotation == null) {
        throw new Error("The given element does not have a rotation attribute.");
    }
    const folder = gui.addFolder(element.name + " rotation" || 'Rotation');
    folder.add(element.rotation, 'x', sliderStart, sliderEnd,step,step);
    folder.add(element.rotation, 'y', sliderStart, sliderEnd,step,step);
    folder.add(element.rotation, 'z', sliderStart, sliderEnd,step,step);
    folder.close();
}

export function createScaleSliders(gui, element, sliderStart, sliderEnd,step = 1) {
    if(element.scale == null) {
        throw new Error("The given element does not have a scale attribute.");
    }
    const folder = gui.addFolder(element.name + " scale" || 'Scale');
    folder.add(element.scale, 'x', sliderStart, sliderEnd,step);
    folder.add(element.scale, 'y', sliderStart, sliderEnd,step);
    folder.add(element.scale, 'z', sliderStart, sliderEnd,step);
    folder.close();
}

export function createAllTransformSliders(gui,element,sliderStart,sliderEnd,step = 1){
    createPositionSliders(gui,element,sliderStart,sliderEnd,step);
    createRotationSliders(gui,element,sliderStart,sliderEnd,step);
    createScaleSliders(gui,element,sliderStart,sliderEnd,step);
}
import * as NGL from "../../../node_modules/ngl/dist/ngl.js"
import {useRef, useEffect} from 'react'

const Viewer = ({protein}) => {
    const ref = useRef(null);
    useEffect(() => {
      if (ref.current) {
        const stage = new NGL.Stage('viewport');
        window.addEventListener('resize', (event) => {
          event.preventDefault();
          stage.handleResize();
        }, false);
        stage.loadFile('rcsb://'+protein, { defaultRepresentation: true });
      }
    }, [ref]);
  
    return (
        <div>
            <center>
                <div id="viewport" ref={ref} style={{ width: '600px', height: '600px' }} />
            </center>
        </div>
    )

}


export default Viewer 
   
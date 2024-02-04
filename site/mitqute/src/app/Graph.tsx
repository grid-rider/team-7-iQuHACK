import React, { useEffect, useRef } from 'react';
import cytoscape, { ElementDefinition } from 'cytoscape';

interface GraphProps {
  elements: ElementDefinition[];
  userEmail: string;
}

const Graph: React.FC<GraphProps> = ({ elements, userEmail }) => {
  const cyRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!cyRef.current) return;

    const cy = cytoscape({
      container: cyRef.current,
      elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#666',
            'color': '#fff',
            'text-valign': 'center',
            'text-halign': 'center',
            'text-outline-color': '#666',
            'text-outline-width': '2px',
            label: 'data(id)',
          },
        },
        {
          selector: 'edge',
          style: {
            width: 3,
            'line-color': '#ccc',
            'curve-style': 'bezier',
            'label': 'data(weight)',
            'text-rotation': 'autorotate',
            'color': '#fff',
            'text-margin-y': '-10px',
          },
        },
        {
          // Change the background color to a vibrant green for the user's node
          selector: `node[id="${userEmail}"]`,
          style: {
            'background-color': '#28B463', // Vibrant green
            'color': '#fff',
            'text-outline-color': '#28B463',
            'text-outline-width': '2px',
            'font-weight': 'bold', // Optionally make the label bold
          },
        },
        {
          selector: 'edge[highlight = 1]',
          style: {
            'line-color': '#007bff',
            width: 4,
          },
        },
      ],
      layout: {
        name: 'circle',
      },
    });

    return () => {
      cy.destroy();
    };
  }, [elements, userEmail]);

  return (
    <>
      <div style={{ width: '600px', height: '600px' }} ref={cyRef}></div>
      <div style={{ marginTop: '20px', color: '#666', textAlign: 'center' }}>
        <p><strong>Legend:</strong></p>
        <p style={{ color: '#28B463' }}>Node with green color is "You"</p>
        <p style={{ color: '#007bff' }}>Edges with blue color represent genuine matches</p>
        <p>Edge labels show the weight or compatibility score</p>
      </div>
    </>
  );
};

export default Graph;

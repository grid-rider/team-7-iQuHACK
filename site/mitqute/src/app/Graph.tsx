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
            'text-margin-y': -10,
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

    cy.on('layoutstop', () => {
        const userNode = cy.elements(`node[id="${userEmail}"]`);
  
        if (userNode) {
          cy.animate({
            center: { eles: userNode },
            zoom: 2 // Adjust zoom level as needed
          }, {
            duration: 1000
          });
        }
    });

    return () => {
      cy.destroy();
    };
  }, [elements, userEmail]);

  return (
    <div className="w-full">
      <h2 className="text-2xl font-semibold text-center text-white mt-12 mb-2">
        Your Quantum Connection Network
      </h2>
      <div className="text-center mb-4 text-gray-200">
        Hold and drag to explore the entangled web of connections.
      </div>
      <div ref={cyRef} style={{height: '600px', width: '600px'}} className="mx-auto shadow rounded-lg p-4"></div>
      <div className="mt-4 text-gray-600 text-center">
        <strong>Legend:</strong>
        <p style={{ color: '#28B463' }}>Node with green color is "You"</p>
        <p style={{ color: '#007bff' }}>Edges with blue color represent genuine matches</p>
        <p>Edge labels show the weight or compatibility score</p>
      </div>
    </div>
  );
};

export default Graph;

import * as React from 'react';

import './GraphMenu.css';

const icons = require('../resources/icons/all.svg') as string;

type Props = {
  undoEnabled: boolean,
  filterUpEnabled: boolean,
  filterDownEnabled: boolean,
  passiveDagButtonEnabled: boolean,
  onUndo: () => void,
  onRenderParentsOnly: () => void,
  onRenderChildrenOnly: () => void,
  onShowPassiveDag: () => void
};

export default class GraphMenu extends React.Component<Props, {}> {

  render() {
    return (
      <div className="component-graph-menu">
        <section className="component-graph-menu-content">
          <button title="Undo last graph transformation" disabled={!this.props.undoEnabled} onClick={this.props.onUndo}>
            <svg viewBox="0 0 24 24" className="icon big">
              <use xlinkHref={`${icons}#graph-undo`}/>
            </svg>
          </button>

          <button title="Render selection only (up)" disabled={!this.props.filterUpEnabled}
                  onClick={this.props.onRenderParentsOnly}>
            <svg viewBox="0 0 24 24" className="icon big">
              <use xlinkHref={`${icons}#graph-up`}/>
            </svg>
          </button>

          <button title="Render selection only (down)" disabled={!this.props.filterDownEnabled}
                  onClick={this.props.onRenderChildrenOnly}>
            <svg viewBox="0 0 24 24" className="icon big">
              <use xlinkHref={`${icons}#graph-down`}/>
            </svg>
          </button>

          <button title="Select clauses"
                  disabled={!this.props.passiveDagButtonEnabled}
                  onClick={() => {
                    this.props.onShowPassiveDag();
                  }}>
            <svg viewBox="0 0 24 24" className="icon big">
              <use xlinkHref={`${icons}#graph-s`}/>
            </svg>
          </button>
        </section>
      </div>
    );
  }
}

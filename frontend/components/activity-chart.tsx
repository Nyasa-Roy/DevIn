const points = [42, 58, 48, 76, 64, 82, 69, 88, 74, 92, 81, 96];

export function ActivityChart() {
  return <div className="chart" aria-label="Commit activity over the last 12 weeks">{points.map((height, index) => <div className="chart-column" key={index}><div className="chart-bar" style={{ height: `${height}%` }} /><span>W{index + 1}</span></div>)}</div>;
}

export function RiskDistribution() {
  return <div className="risk-bars"><div><span><i className="risk-low" />Low <b>54%</b></span><div className="bar-track"><div className="bar-fill risk-low-fill" style={{ width: "54%" }} /></div></div><div><span><i className="risk-medium" />Medium <b>31%</b></span><div className="bar-track"><div className="bar-fill risk-medium-fill" style={{ width: "31%" }} /></div></div><div><span><i className="risk-high" />High <b>15%</b></span><div className="bar-track"><div className="bar-fill risk-high-fill" style={{ width: "15%" }} /></div></div></div>;
}

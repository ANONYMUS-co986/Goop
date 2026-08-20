import { Component } from 'react';

/* ============================================================
 * SAFENET — the blank-page firewall.
 * If ANY runtime error happens anywhere in the app (a shader,
 * a module, a race), React would normally unmount the whole
 * tree → WHITE SCREEN. This boundary catches it and paints a
 * styled recovery screen with a working RELOAD button instead.
 * ============================================================ */
export default class SafeNet extends Component {
  constructor(props) {
    super(props);
    this.state = { broken: false, msg: '' };
  }

  static getDerivedStateFromError(err) {
    return { broken: true, msg: (err && err.message ? err.message : String(err)).slice(0, 160) };
  }

  componentDidCatch(err, info) {
    try { console.error('[SafeNet] caught:', err, info && info.componentStack); } catch (e) { /* noop */ }
  }

  render() {
    if (this.state.broken) {
      return (
        <div style={{
          minHeight: '100vh', display: 'flex', flexDirection: 'column', gap: '18px',
          alignItems: 'center', justifyContent: 'center', textAlign: 'center',
          background: '#040605', color: '#EFE9DC', padding: '30px',
          fontFamily: 'Space Grotesk, system-ui, sans-serif',
        }}>
          <div style={{ fontSize: '52px' }}>🐝</div>
          <h1 style={{ fontFamily: 'Anton, sans-serif', letterSpacing: '.04em', fontSize: 'clamp(26px,4vw,40px)', margin: 0 }}>
            VIKAAS <span style={{ color: '#B9FF3F' }}>//</span> REBOOT
          </h1>
          <p style={{ maxWidth: '46ch', color: '#7d867f', fontSize: '14px', lineHeight: 1.6, margin: 0 }}>
            Something blinked on this page. The drawer is fine — hit reload and it's back.
          </p>
          <code style={{ color: '#B9FF3F', fontSize: '11px', background: '#0a0f0c', border: '1px solid #24302a', padding: '8px 14px', borderRadius: '8px' }}>
            {this.state.msg || 'unknown blip'}
          </code>
          <button
            onClick={() => { this.setState({ broken: false, msg: '' }); }}
            style={{
              background: '#B9FF3F', color: '#040605', border: 'none', borderRadius: '999px',
              padding: '13px 28px', fontWeight: 800, letterSpacing: '.1em', fontSize: '13px',
              cursor: 'pointer', fontFamily: 'inherit',
            }}>
            RELOAD THE DRAWER →
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

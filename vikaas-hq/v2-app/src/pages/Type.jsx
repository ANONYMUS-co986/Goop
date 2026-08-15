import SplitReveal from '../lib/fx/SplitReveal.jsx';
import TextScramble from '../lib/fx/TextScramble.jsx';
import BlurText from '../lib/fx/BlurText.jsx';
import GlitchText from '../lib/fx/GlitchText.jsx';
import SpotlightCard from '../lib/fx/SpotlightCard.jsx';
import './type.css';

/** TYPE — the living styleguide (Phase 2 deliverable).
 *  Shows the full token system + fx library in one scroll. */
export default function Type() {
  return (
    <main className="type-page">
      <section className="type-hero">
        <p className="eyebrow cmd shiny">the styleguide · tokens v2</p>
        <SplitReveal text="TYPE" className="type-big" stagger={0.06} />
        <BlurText text="Every size, every family, every effect — one source of truth." className="type-sub" />
      </section>

      <section className="type-block">
        <p className="eyebrow cmd">the scale</p>
        <div className="type-row"><span className="type-lbl cmd">--fs-hero</span><span className="anton t-hero">VIKAAS विकास</span></div>
        <div className="type-row"><span className="type-lbl cmd">--fs-xlg</span><span className="anton t-xlg">NO DRAWER LEFT BEHIND.</span></div>
        <div className="type-row"><span className="type-lbl cmd">--fs-lg</span><span className="anton t-lg">THE DOORSTEP IS.</span></div>
        <div className="type-row"><span className="type-lbl cmd">--fs-md</span><span className="anton t-md">MISSION TO GENEVA</span></div>
        <div className="type-row"><span className="type-lbl cmd">--fs-body</span><p className="t-body">The drawer had been waiting four years. Inside — 1.4 kg of “kuch kaam ka cheez”. Ten homes asked. Ten drawers found.</p></div>
        <div className="type-row"><span className="type-lbl cmd">--fs-meta</span><span className="cmd t-meta">@QWERTY_AARAV · GURUGRAM · 28.45°N 77.02°E</span></div>
      </section>

      <section className="type-block">
        <p className="eyebrow cmd">the effects</p>
        <div className="fx-grid">
          <SpotlightCard className="fx-cell">
            <p className="cmd fx-tag">SplitReveal</p>
            <SplitReveal text="VIKAAS" className="anton fx-demo" stagger={0.05} />
          </SpotlightCard>
          <SpotlightCard className="fx-cell">
            <p className="cmd fx-tag">TextScramble</p>
            <TextScramble text="SCRAP-SCAN" className="anton fx-demo" />
          </SpotlightCard>
          <SpotlightCard className="fx-cell">
            <p className="cmd fx-tag">BlurText</p>
            <BlurText text="Weighed, not guessed." className="anton fx-demo" />
          </SpotlightCard>
          <SpotlightCard className="fx-cell">
            <p className="cmd fx-tag">GlitchText (hover)</p>
            <GlitchText text="THE DRAWER" className="anton fx-demo" />
          </SpotlightCard>
        </div>
      </section>

      <section className="type-block">
        <p className="eyebrow cmd">the stamps</p>
        <div className="stamp-row">
          <span className="stamp st-green">WEIGHED</span>
          <span className="stamp st-gold">RECEIPT #1</span>
          <span className="stamp st-red">THE GAP</span>
          <span className="stamp st-violet">DRAMATISED</span>
          <span className="stamp st-mute">SOURCED</span>
        </div>
      </section>

      <section className="type-block">
        <p className="eyebrow cmd">text fx utilities</p>
        <p className="t-body"><span className="glow-hover">glow on hover</span> · <span className="shiny">shiny eyebrow</span> · <span className="grad-text anton t-md">gradient big line</span></p>
      </section>
    </main>
  );
}

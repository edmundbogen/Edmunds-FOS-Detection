  """
  Edmund's FOS Detector - Web App Version
  Deployed with Streamlit
  """

  import streamlit as st
  from openai import OpenAI
  from datetime import datetime, timedelta, timezone

  # Page config
  st.set_page_config(
      page_title="Edmund's FOS Detector",
      page_icon="🔍",
      layout="wide"
  )

  # Custom CSS
  st.markdown("""
  <style>
      .main-header {
          font-size: 3rem;
          font-weight: bold;
          color: #1e3a8a;
          text-align: center;
          margin-bottom: 0;
      }
      .sub-header {
          font-size: 1.2rem;
          color: #666;
          text-align: center;
          margin-bottom: 2rem;
      }
      .countdown-box {
          background-color: #000;
          color: #00ff00;
          padding: 10px 20px;
          border-radius: 5px;
          font-family: monospace;
          font-size: 1.2rem;
          display: inline-block;
      }
      .risk-safe { color: #28a745; font-weight: bold; }
      .risk-low { color: #17a2b8; font-weight: bold; }
      .risk-medium { color: #ffc107; font-weight: bold; }
      .risk-high { color: #fd7e14; font-weight: bold; }
      .risk-extreme { color: #dc3545; font-weight: bold; }
  </style>
  """, unsafe_allow_html=True)

  # Initialize session state
  if 'analysis_done' not in st.session_state:
      st.session_state.analysis_done = False
  if 'analysis_result' not in st.session_state:
      st.session_state.analysis_result = None

  def get_next_wednesday_9am_et():
      """Get next Wednesday at 9 AM ET"""
      et = timezone(timedelta(hours=-5))
      now = datetime.now(et)

      days_ahead = 2 - now.weekday()
      if days_ahead <= 0:
          days_ahead += 7

      if now.weekday() == 2 and now.hour >= 9:
          days_ahead = 7

      next_wednesday = now + timedelta(days=days_ahead)
      next_wednesday = next_wednesday.replace(hour=9, minute=0, second=0, microsecond=0)

      return next_wednesday

  def format_countdown():
      """Format countdown to next mastermind"""
      et = timezone(timedelta(hours=-5))
      now = datetime.now(et)
      next_meeting = get_next_wednesday_9am_et()
      time_diff = next_meeting - now

      days = time_diff.days
      hours = time_diff.seconds // 3600
      minutes = (time_diff.seconds % 3600) // 60

      return f"{days}d {hours}h {minutes}m"

  # Header
  st.markdown('<h1 class="main-header">🔍 Edmund\'s FOS Detector</h1>', unsafe_allow_html=True)
  st.markdown('<p class="sub-header">AI-Powered Deception Analysis Tool</p>', unsafe_allow_html=True)

  # Countdown and registration
  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
      st.markdown(f"""
      <div style="text-align: center;">
          <p><strong>Edmund's next Mastermind is in:</strong></p>
          <div class="countdown-box">{format_countdown()}</div>
          <a href="https://www.reignation.com/offers/qLDdFFDo/checkout" target="_blank" 
             style="background-color: #28a745; color: white; padding: 10px 20px; 
                    border-radius: 5px; text-decoration: none; display: inline-block; 
                    margin-left: 10px;">CLICK HERE</a>
      </div>
      """, unsafe_allow_html=True)

  # Sidebar for API key
  with st.sidebar:
      st.header("⚙️ Settings")
      api_key = st.text_input("OpenAI API Key", type="password", help="Your API key is never stored")

      if api_key:
          st.success("✅ API Connected")
          client = OpenAI(api_key=api_key)
      else:
          st.warning("⚠️ Enter your OpenAI API key to enable analysis")
          st.markdown("[Get API Key](https://platform.openai.com/api-keys)")
          client = None

  # Main content area
  st.markdown("---")

  # Input section
  st.subheader("📝 Content to Analyze")

  # Sample text button
  if st.button("Load Sample Scam"):
      st.session_state.text_input = """Dear Valued Investor,

  I am writing to you with an exclusive opportunity that has just become available. As a senior portfolio manager with over 20 
  years of experience on Wall Street, I have access to information that the general public simply doesn't have.

  Our proprietary algorithm has identified a stock that is guaranteed to triple in value within the next 30 days. This is not 
  speculation - this is based on insider knowledge that I am sharing only with my most trusted clients.

  The minimum investment is $10,000, but you must act TODAY. This opportunity will not last, and I can only accept the first 50 
  investors. Wire the funds immediately to secure your position.

  Trust me, you don't want to miss this. I've made millions for my clients using this exact strategy.

  Best regards,
  John Smith
  Senior Portfolio Manager"""

  text_input = st.text_area(
      "Paste or type content here",
      height=300,
      placeholder="Paste the content you want to analyze here (emails, letters, contracts, proposals, etc.)",
      value=st.session_state.get('text_input', '')
  )

  # Buttons
  col1, col2 = st.columns(2)
  with col1:
      analyze_button = st.button("🔍 ANALYZE CONTENT", type="primary", use_container_width=True)
  with col2:
      if st.button("🗑️ CLEAR", type="secondary", use_container_width=True):
          st.session_state.analysis_done = False
          st.session_state.analysis_result = None
          st.session_state.text_input = ""
          st.rerun()

  # Analysis section
  if analyze_button and text_input and client:
      with st.spinner("🤖 AI analyzing content..."):
          try:
              prompt = f"""
  You are Edmund's FOS (Full of S***) Detector - a friendly but sharp-eyed expert at spotting deception, scams, and manipulation. 
  Analyze this content and explain your findings in a conversational, clear way that anyone can understand.

  Text to analyze:
  {text_input[:3000]}

  Please provide:

  1. QUICK TAKE (1-2 sentences)
  Start with your gut reaction - is this legitimate or suspicious?

  2. WHAT I FOUND (conversational explanation)
  Explain in plain English what red flags you spotted. Use phrases like:
  - "Here's what caught my attention..."
  - "The biggest concern is..."
  - "What really stands out is..."
  - "This looks like a classic case of..."

  3. DECEPTION SCORE
  Give a score from 0-100 (0=totally safe, 100=obvious scam)
  Explain what this score means in simple terms.

  4. RISK LEVEL
  Choose one: SAFE / LOW RISK / MEDIUM RISK / HIGH RISK / EXTREME RISK
  Add a brief explanation of what this means for the reader.

  5. MY RECOMMENDATION
  What should the person do? Be specific and actionable.

  6. SUGGESTED RESPONSE (if applicable)
  If this is something that needs a reply (like a suspicious email), provide a professional response template they can use. Start 
  with "If you need to respond, here's what you could say:"

  Make sure to:
  - Use everyday language, not technical jargon
  - Point out specific quotes that are problematic
  - Explain WHY something is a red flag
  - Be helpful and protective, like a knowledgeable friend
  """

              response = client.chat.completions.create(
                  model="gpt-4",
                  messages=[
                      {"role": "system", "content": "You are Edmund's FOS Detector - a friendly, conversational expert who helps 
  people identify scams and deception. You explain things clearly like talking to a friend, avoiding jargon. You're protective and 
  want to keep people safe from being taken advantage of."},
                      {"role": "user", "content": prompt}
                  ],
                  temperature=0.7,
                  max_tokens=1500
              )

              st.session_state.analysis_result = response.choices[0].message.content
              st.session_state.analysis_done = True

          except Exception as e:
              st.error(f"Analysis Error: {str(e)}")

  elif analyze_button and not client:
      st.error("Please enter your OpenAI API key in the sidebar to enable analysis.")
  elif analyze_button and not text_input:
      st.warning("Please enter some content to analyze.")

  # Display results
  if st.session_state.analysis_done and st.session_state.analysis_result:
      st.markdown("---")
      st.markdown("## 🔍 Analysis Results")

      # Display the result
      st.markdown(st.session_state.analysis_result)

      # Add download button for results
      st.download_button(
          label="📥 Download Analysis",
          data=st.session_state.analysis_result,
          file_name=f"fos_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
          mime="text/plain"
      )

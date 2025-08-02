  """
  Edmund's FOS Detector - AI-Powered Edition
  Real deception analysis using OpenAI GPT
  """

  import tkinter as tk
  from tkinter import ttk, scrolledtext, filedialog, messagebox
  import os
  import sys
  from datetime import datetime, timedelta, timezone
  import webbrowser
  import json
  import threading

  # Document parsing imports
  try:
      import PyPDF2
      from docx import Document
      from PIL import Image
      HAS_PDF_SUPPORT = True
  except ImportError:
      HAS_PDF_SUPPORT = False
      print("Note: PDF/Word support not available. Basic text analysis only.")

  # OpenAI import
  try:
      from openai import OpenAI
      HAS_OPENAI = True
  except ImportError:
      HAS_OPENAI = False
      print("Error: OpenAI not installed. Please run: pip3 install --user --break-system-packages openai")

  class FOSDetectorAI:
      def __init__(self, root):
          self.root = root
          self.root.title("Edmund's FOS Detector - AI Edition")
          self.root.geometry("1400x800")
          self.root.minsize(1200, 600)

          # Set background color
          self.root.configure(bg='#f5f7fa')

          # Initialize OpenAI client
          self.openai_client = None
          self.load_api_key()

          # Configure styles
          self.setup_styles()

          # Create main container
          self.create_header()
          self.create_main_content()

      def load_api_key(self):
          """Load API key securely"""
          config_file = "fos_config.txt"
          self.api_key = None
          self.registration_link = "https://example.com/register"

          # First try macOS Keychain (most secure)
          try:
              import subprocess
              result = subprocess.run([
                  'security', 'find-generic-password',
                  '-s', 'FOS_Detector_OpenAI',
                  '-a', 'api_key',
                  '-w'
              ], capture_output=True, text=True)

              if result.returncode == 0:
                  self.api_key = result.stdout.strip()
                  self.openai_client = OpenAI(api_key=self.api_key)
                  print("✅ API key loaded from secure Keychain")
          except:
              pass

          # Try environment variable (second choice)
          if not self.api_key:
              env_key = os.environ.get('OPENAI_API_KEY')
              if env_key:
                  self.api_key = env_key
                  self.openai_client = OpenAI(api_key=self.api_key)
                  print("✅ API key loaded from environment")

          # Load registration link from config
          try:
              if os.path.exists(config_file):
                  with open(config_file, 'r') as f:
                      for line in f:
                          if line.startswith('registration_link='):
                              self.registration_link = line.split('=', 1)[1].strip()
          except Exception as e:
              print(f"Error loading config: {e}")

      def setup_styles(self):
          """Configure custom styles for widgets"""
          self.style = ttk.Style()
          self.style.configure('Custom.TNotebook', background='#f5f7fa')
          self.style.configure('Custom.TNotebook.Tab', padding=[20, 10])

      def create_header(self):
          """Create the header section with countdown"""
          header_frame = tk.Frame(self.root, bg='white', height=100)
          header_frame.pack(fill='x', padx=20, pady=(20, 0))
          header_frame.pack_propagate(False)

          # Left side - Title and subtitle
          left_frame = tk.Frame(header_frame, bg='white')
          left_frame.pack(side='left', fill='y', padx=30)

          title_label = tk.Label(left_frame,
                               text="Edmund's FOS Detector",
                               font=('Arial', 32, 'bold'),
                               bg='white')
          title_label.pack(anchor='w', pady=(20, 5))

          subtitle_label = tk.Label(left_frame,
                                  text="AI-Powered Deception Analysis Tool",
                                  font=('Arial', 16),
                                  fg='#666',
                                  bg='white')
          subtitle_label.pack(anchor='w')

          # Right side - Countdown and register button
          right_frame = tk.Frame(header_frame, bg='white')
          right_frame.pack(side='right', fill='y', padx=30, pady=15)

          container_frame = tk.Frame(right_frame, bg='white')
          container_frame.pack()

          mastermind_label = tk.Label(container_frame,
                                    text="Edmund's next Mastermind is in:",
                                    font=('Arial', 14, 'bold'),
                                    bg='white',
                                    fg='#333333')
          mastermind_label.pack(side='left', padx=(0, 10))

          # Countdown frame
          countdown_frame = tk.Frame(container_frame, bg='white', relief='solid', bd=3,
                                   highlightbackground='#0033FF', highlightthickness=3)
          countdown_frame.pack(side='left', padx=(0, 10))

          self.countdown_label = tk.Label(countdown_frame,
                                        text="00d 00h 00m 00s",
                                        font=('Arial', 16, 'bold'),
                                        bg='white',
                                        fg='#0033FF')
          self.countdown_label.pack(padx=20, pady=10)

          # Register button
          register_frame = tk.Frame(container_frame, bg='white', relief='solid', bd=3,
                                  highlightbackground='#28a745', highlightthickness=3)
          register_frame.pack(side='left')

          self.register_button = tk.Button(register_frame,
                                         text="CLICK HERE",
                                         font=('Arial', 16, 'bold'),
                                         bg='white',
                                         fg='#28a745',
                                         activebackground='#f0f0f0',
                                         activeforeground='#218838',
                                         padx=30,
                                         pady=12,
                                         relief='flat',
                                         bd=0,
                                         cursor='hand2',
                                         command=self.open_registration)
          self.register_button.pack(expand=True)

          # Start countdown
          self.update_countdown()
          self.root.after(1000, self.update_countdown_loop)

      def create_main_content(self):
          """Create the main content area"""
          main_container = tk.Frame(self.root, bg='#f5f7fa')
          main_container.pack(fill='both', expand=True, padx=20, pady=20)

          # Configure grid
          main_container.grid_columnconfigure(0, weight=1, uniform="columns")
          main_container.grid_columnconfigure(1, weight=1, uniform="columns")
          main_container.grid_rowconfigure(0, weight=1)

          # Left column - Content Analysis
          left_frame = tk.Frame(main_container, bg='white', relief='flat')
          left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

          # Right column - Analysis Results
          right_frame = tk.Frame(main_container, bg='white', relief='flat')
          right_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

          self.create_content_analysis(left_frame)
          self.create_analysis_results(right_frame)

      def create_content_analysis(self, parent):
          """Create the content analysis section"""
          container = tk.Frame(parent, bg='white')
          container.pack(fill='both', expand=True)

          # Header
          header_frame = tk.Frame(container, bg='white', padx=30, pady=20)
          header_frame.pack(fill='x')

          icon_label = tk.Label(header_frame, text="📄", font=('Arial', 20), bg='white')
          icon_label.pack(side='left', padx=(0, 10))

          title_label = tk.Label(header_frame,
                               text="Content Analysis",
                               font=('Arial', 18, 'bold'),
                               bg='white')
          title_label.pack(side='left')

          # API Status indicator
          self.api_status = tk.Label(header_frame,
                                   text="🔴 No API Key" if not self.api_key else "🟢 API Connected",
                                   font=('Arial', 10),
                                   bg='white')
          self.api_status.pack(side='right')

          desc_label = tk.Label(container,
                              text="Upload documents or paste text to analyze for deception indicators",
                              font=('Arial', 12),
                              fg='#666',
                              bg='white')
          desc_label.pack(anchor='w', padx=30, pady=(0, 20))

          # Notebook
          notebook_frame = tk.Frame(container, bg='white', height=400)
          notebook_frame.pack(fill='both', expand=True, padx=30)
          notebook_frame.pack_propagate(False)

          notebook = ttk.Notebook(notebook_frame, style='Custom.TNotebook')
          notebook.pack(fill='both', expand=True)

          # Text Input tab
          text_tab = tk.Frame(notebook, bg='white')
          notebook.add(text_tab, text="Text Input")

          # File Upload tab
          file_tab = tk.Frame(notebook, bg='white')
          notebook.add(file_tab, text="File Upload")

          self.create_text_input_section(text_tab)
          self.create_file_upload_section(file_tab)

          # Buttons
          button_frame = tk.Frame(container, bg='white', height=100)
          button_frame.pack(fill='x', padx=30, pady=(10, 20))
          button_frame.pack_propagate(False)

          inner_button_frame = tk.Frame(button_frame, bg='white')
          inner_button_frame.pack(expand=True, fill='both', padx=10, pady=15)

          # Analyze button
          self.analyze_button = tk.Button(inner_button_frame,
                                        text="🔍 ANALYZE CONTENT",
                                        font=('Arial', 18, 'bold'),
                                        bg='white',
                                        fg='#0033FF',
                                        activebackground='#f0f0f0',
                                        activeforeground='#002299',
                                        padx=40,
                                        pady=20,
                                        relief='solid',
                                        bd=4,
                                        highlightcolor='#0033FF',
                                        highlightbackground='#0033FF',
                                        highlightthickness=4,
                                        cursor='hand2',
                                        command=self.analyze_content)
          self.analyze_button.pack(side='left', expand=True, fill='both', padx=(0, 10))

          # Clear button
          self.clear_button = tk.Button(inner_button_frame,
                                      text="🗑️ CLEAR",
                                      font=('Arial', 18, 'bold'),
                                      bg='white',
                                      fg='#CC0000',
                                      activebackground='#f0f0f0',
                                      activeforeground='#990000',
                                      padx=40,
                                      pady=20,
                                      relief='solid',
                                      bd=4,
                                      highlightcolor='#CC0000',
                                      highlightbackground='#CC0000',
                                      highlightthickness=4,
                                      cursor='hand2',
                                      command=self.clear_content)
          self.clear_button.pack(side='right', expand=True, fill='both', padx=(10, 0))

          # Hover effects
          self.analyze_button.bind('<Enter>', lambda e: self.analyze_button.config(bg='#e6f2ff'))
          self.analyze_button.bind('<Leave>', lambda e: self.analyze_button.config(bg='white'))
          self.clear_button.bind('<Enter>', lambda e: self.clear_button.config(bg='#ffe6e6'))
          self.clear_button.bind('<Leave>', lambda e: self.clear_button.config(bg='white'))

      def create_text_input_section(self, parent):
          """Create the text input section"""
          frame = tk.Frame(parent, bg='white', padx=20, pady=20)
          frame.pack(fill='both', expand=True)

          label = tk.Label(frame,
                         text="Content to Analyze",
                         font=('Arial', 14, 'bold'),
                         bg='white')
          label.pack(anchor='w', pady=(0, 10))

          sample_button = tk.Button(frame,
                                  text="Load Sample",
                                  font=('Arial', 11),
                                  relief='flat',
                                  bg='#f8f9fa',
                                  cursor='hand2',
                                  command=self.load_sample)
          sample_button.pack(anchor='e', pady=(0, 10))

          self.text_input = scrolledtext.ScrolledText(frame,
                                                     wrap=tk.WORD,
                                                     height=10,
                                                     font=('Arial', 12),
                                                     relief='solid',
                                                     borderwidth=1)
          self.text_input.pack(fill='both', expand=True)

          placeholder = "Paste the content you want to analyze here (emails, letters, contracts, proposals, etc.)"
          self.text_input.insert('1.0', placeholder)
          self.text_input.config(fg='#999')

          self.text_input.bind('<FocusIn>', self.on_text_focus_in)
          self.text_input.bind('<FocusOut>', self.on_text_focus_out)

      def create_file_upload_section(self, parent):
          """Create the file upload section"""
          frame = tk.Frame(parent, bg='white')
          frame.pack(fill='both', expand=True)

          upload_frame = tk.Frame(frame, bg='#f8f9fa', relief='solid', borderwidth=2)
          upload_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=300)

          icon_label = tk.Label(upload_frame, text="📁", font=('Arial', 48), bg='#f8f9fa')
          icon_label.pack(pady=(50, 20))

          upload_button = tk.Button(upload_frame,
                                  text="Choose Files",
                                  font=('Arial', 12),
                                  bg='white',
                                  relief='solid',
                                  borderwidth=1,
                                  padx=20,
                                  pady=10,
                                  cursor='hand2',
                                  command=self.upload_file)
          upload_button.pack()

          or_label = tk.Label(upload_frame,
                            text="Supports: PDF, Word, TXT, Images",
                            font=('Arial', 11),
                            fg='#666',
                            bg='#f8f9fa')
          or_label.pack(pady=(10, 0))

          self.uploaded_file_path = None

      def create_analysis_results(self, parent):
          """Create the analysis results section"""
          header_frame = tk.Frame(parent, bg='white', padx=30, pady=20)
          header_frame.pack(fill='x')

          title_label = tk.Label(header_frame,
                               text="Analysis Results",
                               font=('Arial', 18, 'bold'),
                               bg='white')
          title_label.pack(anchor='w')

          desc_label = tk.Label(parent,
                              text="AI-powered analysis results will appear here",
                              font=('Arial', 12),
                              fg='#666',
                              bg='white')
          desc_label.pack(anchor='w', padx=30, pady=(0, 20))

          results_frame = tk.Frame(parent, bg='#f8f9fa')
          results_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))

          placeholder_frame = tk.Frame(results_frame, bg='#f8f9fa')
          placeholder_frame.place(relx=0.5, rely=0.5, anchor='center')

          icon_label = tk.Label(placeholder_frame, text="🤖", font=('Arial', 64), bg='#f8f9fa', fg='#ddd')
          icon_label.pack()

          ready_label = tk.Label(placeholder_frame,
                               text="AI Ready to Analyze",
                               font=('Arial', 20),
                               fg='#999',
                               bg='#f8f9fa')
          ready_label.pack(pady=(20, 10))

          info_label = tk.Label(placeholder_frame,
                              text="Paste content or upload files to get started",
                              font=('Arial', 12),
                              fg='#aaa',
                              bg='#f8f9fa')
          info_label.pack()

          self.results_frame = results_frame
          self.placeholder_frame = placeholder_frame
          self.results_display = None

      def analyze_content(self):
          """Analyze content using OpenAI"""
          if not self.api_key:
              messagebox.showerror("API Key Required",
                                 "Please add your OpenAI API key to fos_config.txt\n\n" +
                                 "Get your key from: https://platform.openai.com/api-keys")
              return

          content = self.get_content_to_analyze()
          if not content:
              messagebox.showwarning("No Content", "Please enter some content to analyze.")
              return

          # Show loading
          self.show_loading()

          # Run analysis in thread to prevent UI freeze
          thread = threading.Thread(target=self.run_ai_analysis, args=(content,))
          thread.start()

      def get_content_to_analyze(self):
          """Get content from text input or uploaded file"""
          # Check if there's an uploaded file
          if hasattr(self, 'uploaded_file_content') and self.uploaded_file_content:
              return self.uploaded_file_content

          # Otherwise get from text input
          content = self.text_input.get('1.0', 'end-1c').strip()
          placeholder = "Paste the content you want to analyze here (emails, letters, contracts, proposals, etc.)"

          if content and content != placeholder:
              return content
          return None

      def run_ai_analysis(self, content):
          """Run the actual AI analysis"""
          try:
              prompt = f"""
  You are Edmund's FOS (Full of S***) Detector - a friendly but sharp-eyed expert at spotting deception, scams, and manipulation. 
  Analyze this content and explain your findings in a conversational, clear way that anyone can understand.

  Text to analyze:
  {content[:3000]}  # Limit to 3000 chars to save tokens

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

              response = self.openai_client.chat.completions.create(
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

              result = response.choices[0].message.content

              # Update UI in main thread
              self.root.after(0, self.show_results, result)

          except Exception as e:
              error_msg = f"Analysis Error: {str(e)}"
              self.root.after(0, self.show_error, error_msg)

      def show_loading(self):
          """Show loading indicator"""
          if self.placeholder_frame:
              self.placeholder_frame.destroy()

          loading_frame = tk.Frame(self.results_frame, bg='#f8f9fa')
          loading_frame.place(relx=0.5, rely=0.5, anchor='center')

          loading_label = tk.Label(loading_frame,
                                 text="🔄 AI Analyzing Content...",
                                 font=('Arial', 16),
                                 bg='#f8f9fa')
          loading_label.pack()

          self.loading_frame = loading_frame

      def show_results(self, analysis_text):
          """Display AI analysis results"""
          if hasattr(self, 'loading_frame'):
              self.loading_frame.destroy()

          if self.placeholder_frame:
              self.placeholder_frame.destroy()

          # Create results display
          results_display = scrolledtext.ScrolledText(self.results_frame,
                                                    wrap=tk.WORD,
                                                    font=('Arial', 12),
                                                    bg='white',
                                                    relief='flat')
          results_display.pack(fill='both', expand=True, padx=20, pady=20)

          # Add friendly header
          timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          header = f"🔍 Edmund's FOS Detector Analysis\n"
          header += f"Analyzed at: {timestamp}\n"
          header += f"{'-'*60}\n\n"

          results_display.insert('1.0', header + analysis_text)

          # Add visual formatting for suggested response
          if "SUGGESTED RESPONSE" in analysis_text:
              # This will help highlight the suggested response section
              results_display.tag_add("response", "1.0", "end")
              results_display.tag_config("response", font=('Arial', 12))
          results_display.config(state='disabled')

          self.results_display = results_display

      def show_error(self, error_msg):
          """Show error message"""
          if hasattr(self, 'loading_frame'):
              self.loading_frame.destroy()

          messagebox.showerror("Analysis Error", error_msg)

      def upload_file(self):
          """Handle file upload with multiple format support"""
          filename = filedialog.askopenfilename(
              title="Select file to analyze",
              filetypes=[
                  ("All Supported", "*.txt;*.pdf;*.docx;*.doc;*.png;*.jpg;*.jpeg"),
                  ("Text files", "*.txt"),
                  ("PDF files", "*.pdf"),
                  ("Word files", "*.docx;*.doc"),
                  ("Images", "*.png;*.jpg;*.jpeg"),
                  ("All files", "*.*")
              ]
          )

          if filename:
              try:
                  # Extract text based on file type
                  ext = os.path.splitext(filename)[1].lower()

                  if ext == '.txt':
                      with open(filename, 'r', encoding='utf-8') as f:
                          content = f.read()

                  elif ext == '.pdf':
                      content = self.extract_pdf_text(filename)

                  elif ext in ['.docx', '.doc']:
                      content = self.extract_word_text(filename)

                  elif ext in ['.png', '.jpg', '.jpeg']:
                      content = self.extract_image_text(filename)

                  else:
                      messagebox.showwarning("Unsupported Format",
                                           "This file format is not yet supported.")
                      return

                  # Store the content
                  self.uploaded_file_content = content

                  # Update text input to show preview
                  self.text_input.delete('1.0', 'end')
                  preview = content[:500] + "..." if len(content) > 500 else content
                  self.text_input.insert('1.0', f"[Uploaded: {os.path.basename(filename)}]\n\n{preview}")

                  messagebox.showinfo("File Uploaded",
                                    f"Successfully loaded: {os.path.basename(filename)}\n" +
                                    f"Content length: {len(content)} characters")

              except Exception as e:
                  messagebox.showerror("Upload Error", f"Failed to read file: {str(e)}")

      def extract_pdf_text(self, filepath):
          """Extract text from PDF"""
          text = ""
          with open(filepath, 'rb') as file:
              pdf_reader = PyPDF2.PdfReader(file)
              for page in pdf_reader.pages:
                  text += page.extract_text() + "\n"
          return text

      def extract_word_text(self, filepath):
          """Extract text from Word document"""
          doc = Document(filepath)
          text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
          return text

      def extract_image_text(self, filepath):
          """Extract text from image using OCR"""
          return "[OCR not available - text extraction from images not supported]"

      def clear_content(self):
          """Clear all content and reset"""
          self.text_input.delete('1.0', 'end')
          self.text_input.insert('1.0', "Paste the content you want to analyze here (emails, letters, contracts, proposals, etc.)")
          self.text_input.config(fg='#999')

          # Clear uploaded file
          self.uploaded_file_content = None

          # Clear results
          if self.results_display:
              self.results_display.destroy()
              self.results_display = None

          # Recreate placeholder
          if hasattr(self, 'placeholder_frame') and self.placeholder_frame:
              try:
                  self.placeholder_frame.destroy()
              except:
                  pass

          placeholder_frame = tk.Frame(self.results_frame, bg='#f8f9fa')
          placeholder_frame.place(relx=0.5, rely=0.5, anchor='center')

          icon_label = tk.Label(placeholder_frame, text="🤖", font=('Arial', 64), bg='#f8f9fa', fg='#ddd')
          icon_label.pack()

          ready_label = tk.Label(placeholder_frame,
                               text="AI Ready to Analyze",
                               font=('Arial', 20),
                               fg='#999',
                               bg='#f8f9fa')
          ready_label.pack(pady=(20, 10))

          info_label = tk.Label(placeholder_frame,
                              text="Paste content or upload files to get started",
                              font=('Arial', 12),
                              fg='#aaa',
                              bg='#f8f9fa')
          info_label.pack()

          self.placeholder_frame = placeholder_frame

      def load_sample(self):
          """Load sample text"""
          sample_text = """Dear Valued Investor,

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

          self.text_input.config(fg='black')
          self.text_input.delete('1.0', 'end')
          self.text_input.insert('1.0', sample_text)
          self.uploaded_file_content = None

      def on_text_focus_in(self, event):
          """Handle focus in"""
          if self.text_input.get('1.0', 'end-1c') == "Paste the content you want to analyze here (emails, letters, contracts, 
  proposals, etc.)":
              self.text_input.delete('1.0', 'end')
              self.text_input.config(fg='black')

      def on_text_focus_out(self, event):
          """Handle focus out"""
          if self.text_input.get('1.0', 'end-1c').strip() == '':
              self.text_input.insert('1.0', "Paste the content you want to analyze here (emails, letters, contracts, proposals, 
  etc.)")
              self.text_input.config(fg='#999')

      # Countdown methods
      def get_next_wednesday_9am_et(self):
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

      def update_countdown(self):
          """Update countdown display"""
          try:
              et = timezone(timedelta(hours=-5))
              now = datetime.now(et)
              next_meeting = self.get_next_wednesday_9am_et()
              time_diff = next_meeting - now

              days = time_diff.days
              hours = time_diff.seconds // 3600
              minutes = (time_diff.seconds % 3600) // 60
              seconds = time_diff.seconds % 60

              countdown_text = f"{days:02d}d {hours:02d}h {minutes:02d}m {seconds:02d}s"
              self.countdown_label.config(text=countdown_text)

          except Exception as e:
              self.countdown_label.config(text="Error")

      def update_countdown_loop(self):
          """Update countdown every second"""
          self.update_countdown()
          self.root.after(1000, self.update_countdown_loop)

      def open_registration(self):
          """Open registration link"""
          webbrowser.open(self.registration_link)

      def load_registration_link(self):
          """Load registration link from config file"""
          config_file = "fos_config.txt"
          default_link = "https://example.com/register"

          try:
              if os.path.exists(config_file):
                  with open(config_file, 'r') as f:
                      for line in f:
                          if line.startswith('registration_link='):
                              self.registration_link = line.split('=', 1)[1].strip()
                              return
              self.registration_link = default_link
          except:
              self.registration_link = default_link

  if __name__ == "__main__":
      root = tk.Tk()
      app = FOSDetectorAI(root)
      root.mainloop()

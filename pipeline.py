import uuid
import time
import asyncio
from services_livekit import LiveKitService
from services_deepgram import DeepgramService
from services_groq import GroqService
from services_elevenlabs import ElevenLabsService
from metrics import log_session_metrics

class AgentSession:
    def __init__(self, livekit, deepgram, groq, elevenlabs):
        self.livekit = livekit
        self.deepgram = deepgram
        self.groq = groq
        self.elevenlabs = elevenlabs
        self.session_id = str(uuid.uuid4())
        self.conversation = []
        self.running = True
        
    async def run(self):
        """Main conversation loop"""
        print(f"Starting Agent Session: {self.session_id}")
        print("Say something to start the conversation...")
          # Connect to services
        await self.livekit.connect()
        
        turn_count = 0
        while self.running:  # Run continuously
            try:
                print(f"\n--- Turn {turn_count + 1} ---")
                await self.process_turn()
                turn_count += 1
                
                # Small delay between turns
                await asyncio.sleep(1)
                    
            except KeyboardInterrupt:
                print("\nConversation interrupted by user")
                break
            except Exception as e:
                print(f"Error in conversation turn: {e}")
                # Continue on error after a short delay
                await asyncio.sleep(2)
        
        await self.livekit.disconnect()
        print(f"Session {self.session_id} ended")
        
    async def process_turn(self):
        """Process a single conversation turn"""
        start_time = time.time()
        
        # Step 1: Receive audio input
        print("🎤 Recording... (5 seconds)")
        audio_data = self.livekit.receive_audio()
        if not audio_data:
            print("No audio received")
            return
            
        # Step 2: Transcribe audio
        print("🔄 Transcribing...")
        t0 = time.time()
        transcript = await self.deepgram.transcribe(audio_data)
        t1 = time.time()
        
        if not transcript.strip():
            print("No speech detected")
            return
            
        print(f"👤 User: {transcript}")
        
        # Step 3: Generate response
        print("🧠 Generating response...")
        response = self.groq.generate_response(transcript)
        t2 = time.time()
        
        print(f"🤖 Agent: {response}")
        
        # Step 4: Synthesize speech
        print("🔊 Synthesizing speech...")
        audio_response = self.elevenlabs.synthesize(response)
        t3 = time.time()
        
        # Step 5: Play audio response
        print("📢 Playing response...")
        self.livekit.send_audio(audio_response)
        t4 = time.time()
        
        # Calculate metrics
        e2e_delay = t4 - start_time
        tift = t1 - t0  # Time in transcription
        ttfb = t2 - t1  # Time to first byte (LLM response)
        total_latency = t3 - t0  # Total processing latency
        usage_summary = f"Input: {len(transcript)} chars, Output: {len(response)} chars"
        
        # Store conversation
        self.conversation.append((transcript, response))
        
        # Generate summary
        summary = self.summarize_conversation()
        
        # Log metrics
        log_session_metrics(
            self.session_id, 
            e2e_delay, 
            tift, 
            ttfb, 
            total_latency, 
            usage_summary, 
            summary
        )
        
        # Print metrics
        print(f"\n📊 Metrics:")
        print(f"   E2E Delay: {e2e_delay:.2f}s")
        print(f"   TIFT: {tift:.2f}s")
        print(f"   TTFB: {ttfb:.2f}s")
        print(f"   Total Latency: {total_latency:.2f}s")
        
    def summarize_conversation(self):
        """Create a summary of the conversation"""
        if not self.conversation:
            return "No conversation yet"
        
        # Simple summary: concatenate all exchanges
        summary_parts = []
        for i, (user_text, agent_text) in enumerate(self.conversation, 1):
            summary_parts.append(f"Turn {i} - User: {user_text[:50]}... Agent: {agent_text[:50]}...")
        
        return " | ".join(summary_parts)
    
    def stop(self):
        """Stop the conversation"""
        self.running = False

import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String selectedLanguage = 'en';
  
  final Map<String, String> languages = {
    'en': 'English',
    'hi': 'हिंदी',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'bn': 'বাংলা',
    'mr': 'मराठी',
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart Shiksha'),
        actions: [
          // Language Selector
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: DropdownButton<String>(
              value: selectedLanguage,
              dropdownColor: const Color(0xFF222222),
              style: const TextStyle(color: Color(0xFF0EA5E9)),
              underline: Container(),
              items: languages.entries.map((entry) {
                return DropdownMenuItem(
                  value: entry.key,
                  child: Text(entry.value),
                );
              }).toList(),
              onChanged: (value) {
                if (value != null) {
                  setState(() {
                    selectedLanguage = value;
                  });
                }
              },
            ),
          ),
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Welcome to AI Tutor',
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFFCAF0F8),
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 10),
              const Text(
                'Hello, Student! Ready to learn today?',
                style: TextStyle(fontSize: 18, color: Colors.white70),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 60),
              
              // Navigation Cards
              Wrap(
                spacing: 20,
                runSpacing: 20,
                alignment: WrapAlignment.center,
                children: [
                  _buildNavCard(
                    context,
                    'Lessons',
                    'Explore personalized lessons tailored for you.',
                    Icons.book,
                    '/lessons',
                  ),
                  _buildNavCard(
                    context,
                    'Quizzes',
                    'Test your knowledge with adaptive quizzes.',
                    Icons.quiz,
                    '/quiz',
                  ),
                  _buildNavCard(
                    context,
                    'AI Chat',
                    'Ask your AI tutor anything!',
                    Icons.chat,
                    '/chat',
                  ),
                  _buildNavCard(
                    context,
                    'Progress',
                    'Track your learning journey.',
                    Icons.show_chart,
                    '/progress',
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNavCard(
    BuildContext context,
    String title,
    String description,
    IconData icon,
    String route,
  ) {
    return SizedBox(
      width: 220,
      child: Card(
        color: const Color(0xFF222222),
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
          side: const BorderSide(color: Color(0xFF555555)),
        ),
        child: InkWell(
          onTap: () {
            if (route == '/progress') {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Coming soon!')),
              );
            } else {
              Navigator.pushNamed(context, route);
            }
          },
          borderRadius: BorderRadius.circular(8),
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(icon, size: 48, color: const Color(0xFF0EA5E9)),
                const SizedBox(height: 15),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 10),
                Text(
                  description,
                  style: const TextStyle(
                    fontSize: 14,
                    color: Colors.white70,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 15),
                ElevatedButton(
                  onPressed: () {
                    if (route == '/progress') {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Coming soon!')),
                      );
                    } else {
                      Navigator.pushNamed(context, route);
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF0EA5E9),
                    foregroundColor: Colors.white,
                  ),
                  child: const Text('Go'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

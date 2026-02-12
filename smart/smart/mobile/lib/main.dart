import 'package:flutter/material.dart';

void main() {
  runApp(const SmartShikshaApp());
}

class SmartShikshaApp extends StatelessWidget {
  const SmartShikshaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Shiksha',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0D9488)),
        useMaterial3: true,
      ),
      home: const AppShell(),
    );
  }
}

class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _selectedIndex = 0;

  static const List<Widget> _screens = <Widget>[
    HomeScreen(),
    TutorScreen(),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (value) => setState(() => _selectedIndex = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.chat_bubble_outline), label: 'Tutor'),
          NavigationDestination(icon: Icon(Icons.person_outline), label: 'Profile'),
        ],
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text('Continue Learning', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w700)),
          const SizedBox(height: 12),
          Card(
            child: ListTile(
              title: const Text('Mathematics: Linear Equations'),
              subtitle: const Text('Resume lesson 3 of chapter 5'),
              trailing: FilledButton(
                onPressed: () {},
                child: const Text('Open'),
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: ListTile(
              leading: const Icon(Icons.local_fire_department_outlined),
              title: const Text('Daily Streak'),
              subtitle: const Text('5 days in a row'),
            ),
          ),
        ],
      ),
    );
  }
}

class TutorScreen extends StatelessWidget {
  const TutorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(16),
            child: Text('AI Tutor', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w700)),
          ),
          const Expanded(
            child: Center(
              child: Text('WhatsApp-style chat list placeholder'),
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(12, 0, 12, 12),
            child: Row(
              children: [
                IconButton(
                  onPressed: () {},
                  icon: const Icon(Icons.camera_alt_outlined),
                  tooltip: 'Snap Question (OCR)',
                ),
                const Expanded(
                  child: TextField(
                    decoration: InputDecoration(
                      hintText: 'Ask your tutor...',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                IconButton(
                  onPressed: () {},
                  icon: const Icon(Icons.mic_none_outlined),
                  tooltip: 'Voice Input',
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Text('Profile', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w700)),
          SizedBox(height: 16),
          Card(
            child: ListTile(
              title: Text('Subject Strengths'),
              subtitle: Text('Spider-chart placeholder for Math/Science/English/Social Studies'),
            ),
          ),
        ],
      ),
    );
  }
}

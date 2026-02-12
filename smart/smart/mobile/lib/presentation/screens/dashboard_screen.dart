import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart Shiksha Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.sync),
            onPressed: () {
              // Trigger sync manually
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Syncing data...')),
              );
            },
          )
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildDailyStreakCard(),
              const SizedBox(height: 16),
              const Text(
                'Performance Overview',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              _buildPerformanceGraphPlaceholder(),
              const SizedBox(height: 16),
              const Text(
                'Recommended for You',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              _buildRecommendationList(context),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.quiz), label: 'Practice'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
        onTap: (index) {
          if (index == 1) {
            Navigator.pushNamed(context, '/quiz');
          }
        },
      ),
    );
  }

  Widget _buildDailyStreakCard() {
    return Card(
      color: Colors.orangeAccent.shade100,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text('Daily Streak', style: TextStyle(fontWeight: FontWeight.bold)),
                Text('5 Days', style: TextStyle(fontSize: 24, color: Colors.deepOrange)),
              ],
            ),
            const Icon(Icons.local_fire_department, color: Colors.deepOrange, size: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildPerformanceGraphPlaceholder() {
    return Card(
      child: Container(
        height: 200,
        width: double.infinity,
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text('Subject Strength'),
            Expanded(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildBar('Math', 0.8, Colors.blue),
                  _buildBar('Physics', 0.6, Colors.green),
                  _buildBar('Chem', 0.4, Colors.red),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildBar(String label, double heightPct, Color color) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        Container(
          width: 30,
          height: 150 * heightPct,
          color: color,
        ),
        const SizedBox(height: 4),
        Text(label),
      ],
    );
  }

  Widget _buildRecommendationList(BuildContext context) {
    final recommendations = [
      {'title': 'Newton\'s Laws', 'subject': 'Physics'},
      {'title': 'Organic Compounds', 'subject': 'Chemistry'},
      {'title': 'Calculus Verification', 'subject': 'Math'},
    ];

    return Column(
      children: recommendations.map((r) {
        return Card(
          child: ListTile(
            leading: const Icon(Icons.book),
            title: Text(r['title']!),
            subtitle: Text(r['subject']!),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
               // Navigation to Lesson
            },
          ),
        );
      }).toList(),
    );
  }
}

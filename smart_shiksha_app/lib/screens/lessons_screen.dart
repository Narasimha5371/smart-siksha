import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';

class LessonsScreen extends StatefulWidget {
  const LessonsScreen({super.key});

  @override
  State<LessonsScreen> createState() => _LessonsScreenState();
}

class _LessonsScreenState extends State<LessonsScreen> {
  List<String> _subjects = [];
  bool _isLoading = true;
  String? _selectedSubject;
  List<String> _topics = [];

  @override
  void initState() {
    super.initState();
    _loadSubjects();
  }

  Future<void> _loadSubjects() async {
    final apiService = context.read<ApiService>();
    final subjects = await apiService.getSubjects();
    setState(() {
      _subjects = subjects;
      _isLoading = false;
    });
  }

  Future<void> _loadTopics(String subject) async {
    setState(() {
      _selectedSubject = subject;
      _isLoading = true;
    });

    final apiService = context.read<ApiService>();
    final topics = await apiService.getTopics(subject);

    setState(() {
      _topics = topics;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lessons'),
        actions: [
          if (_selectedSubject != null)
            IconButton(
              icon: const Icon(Icons.close),
              onPressed: () {
                setState(() {
                  _selectedSubject = null;
                  _topics = [];
                });
              },
            ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _selectedSubject == null
              ? _buildSubjectsGrid()
              : _buildTopicsList(),
    );
  }

  Widget _buildSubjectsGrid() {
    return GridView.builder(
      padding: const EdgeInsets.all(16),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        childAspectRatio: 1.2,
      ),
      itemCount: _subjects.length,
      itemBuilder: (context, index) {
        final subject = _subjects[index];
        return Card(
          color: const Color(0xFF222222),
          elevation: 4,
          child: InkWell(
            onTap: () => _loadTopics(subject),
            borderRadius: BorderRadius.circular(8),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    _getSubjectIcon(subject),
                    size: 48,
                    color: const Color(0xFF0EA5E9),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    subject,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                    textAlign: TextAlign.center,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildTopicsList() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _topics.length,
      itemBuilder: (context, index) {
        final topic = _topics[index];
        return Card(
          color: const Color(0xFF222222),
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            leading: const Icon(
              Icons.topic,
              color: Color(0xFF0EA5E9),
            ),
            title: Text(
              topic,
              style: const TextStyle(color: Colors.white),
            ),
            trailing: const Icon(
              Icons.arrow_forward_ios,
              color: Colors.white54,
              size: 16,
            ),
            onTap: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Topic: $topic')),
              );
            },
          ),
        );
      },
    );
  }

  IconData _getSubjectIcon(String subject) {
    final subjectLower = subject.toLowerCase();
    if (subjectLower.contains('anatomy')) return Icons.accessibility;
    if (subjectLower.contains('medicine')) return Icons.medical_services;
    if (subjectLower.contains('surgery')) return Icons.healing;
    if (subjectLower.contains('pharmacology')) return Icons.medication;
    if (subjectLower.contains('bio')) return Icons.biotech;
    if (subjectLower.contains('chem')) return Icons.science;
    if (subjectLower.contains('physic')) return Icons.psychology;
    return Icons.school;
  }
}

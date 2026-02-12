import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/question.dart';

class ApiService {
  // Change this to your backend URL
  // For local development: http://localhost:8000
  // For production: https://your-backend-url.com
  static const String baseUrl = 'http://localhost:8000';
  
  // Chat with AI tutor
  Future<String> chat(String message, String language) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': message,
          'language': language,
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['answer'] ?? 'No response';
      } else {
        return 'Error: ${response.statusCode}';
      }
    } catch (e) {
      return 'Failed to connect to server. Please check your connection.';
    }
  }
  
  // Get list of subjects
  Future<List<String>> getSubjects() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/subjects'));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<String>.from(data['subjects'] ?? []);
      }
      return [];
    } catch (e) {
      return [];
    }
  }
  
  // Get topics for a subject
  Future<List<String>> getTopics(String subject) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/topics/$subject'),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<String>.from(data['topics'] ?? []);
      }
      return [];
    } catch (e) {
      return [];
    }
  }
  
  // Generate quiz
  Future<List<Question>> generateQuiz({
    String? subject,
    int numQuestions = 10,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/quiz/generate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'subject': subject,
          'num_questions': numQuestions,
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final questions = data['questions'] as List;
        return questions.map((q) => Question.fromJson(q)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }
  
  // Translate text
  Future<String> translate(
    String text,
    String sourceLang,
    String targetLang,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/translate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'text': text,
          'source_lang': sourceLang,
          'target_lang': targetLang,
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['translated_text'] ?? text;
      }
      return text;
    } catch (e) {
      return text;
    }
  }
  
  // Get supported languages
  Future<Map<String, String>> getLanguages() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/languages'));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return Map<String, String>.from(data);
      }
      return {'en': 'English'};
    } catch (e) {
      return {'en': 'English'};
    }
  }
  
  // Health check
  Future<bool> checkHealth() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/health'),
      ).timeout(const Duration(seconds: 5));
      
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

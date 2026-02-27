import 'dart:convert';
import 'dart:developer' as developer;
import 'package:http/http.dart' as http;
import '../models/question.dart';

class ApiService {
  // Change this to your backend URL
  // For local development: http://localhost:8000
  // For production: https://your-backend-url.com
  static const String baseUrl = 'http://localhost:8000';
  
  final http.Client _client;

  ApiService({http.Client? client}) : _client = client ?? http.Client();

  // Chat with AI tutor
  Future<String> chat(String message, String language) async {
    try {
      final response = await _client.post(
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
        developer.log('Chat API Error: ${response.statusCode}', name: 'ApiService');
        return 'Error: ${response.statusCode}';
      }
    } catch (e) {
      developer.log('Chat API Exception: $e', name: 'ApiService', error: e);
      return 'Failed to connect to server. Please check your connection.';
    }
  }
  
  // Get list of subjects
  Future<List<String>> getSubjects() async {
    try {
      final response = await _client.get(Uri.parse('$baseUrl/subjects'));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<String>.from(data['subjects'] ?? []);
      }
      developer.log('GetSubjects API Error: ${response.statusCode}', name: 'ApiService');
      return [];
    } catch (e) {
      developer.log('GetSubjects API Exception: $e', name: 'ApiService', error: e);
      return [];
    }
  }
  
  // Get topics for a subject
  Future<List<String>> getTopics(String subject) async {
    try {
      final response = await _client.get(
        Uri.parse('$baseUrl/topics/$subject'),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<String>.from(data['topics'] ?? []);
      }
      developer.log('GetTopics API Error: ${response.statusCode}', name: 'ApiService');
      return [];
    } catch (e) {
      developer.log('GetTopics API Exception: $e', name: 'ApiService', error: e);
      return [];
    }
  }
  
  // Generate quiz
  Future<List<Question>> generateQuiz({
    String? subject,
    int numQuestions = 10,
  }) async {
    try {
      final response = await _client.post(
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
      developer.log('GenerateQuiz API Error: ${response.statusCode}', name: 'ApiService');
      return [];
    } catch (e) {
      developer.log('GenerateQuiz API Exception: $e', name: 'ApiService', error: e);
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
      final response = await _client.post(
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
      developer.log('Translate API Error: ${response.statusCode}', name: 'ApiService');
      return text;
    } catch (e) {
      developer.log('Translate API Exception: $e', name: 'ApiService', error: e);
      return text;
    }
  }
  
  // Get supported languages
  Future<Map<String, String>> getLanguages() async {
    try {
      final response = await _client.get(Uri.parse('$baseUrl/languages'));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return Map<String, String>.from(data);
      }
      developer.log('GetLanguages API Error: ${response.statusCode}', name: 'ApiService');
      return {'en': 'English'};
    } catch (e) {
      developer.log('GetLanguages API Exception: $e', name: 'ApiService', error: e);
      return {'en': 'English'};
    }
  }
  
  // Health check
  Future<bool> checkHealth() async {
    try {
      final response = await _client.get(
        Uri.parse('$baseUrl/health'),
      ).timeout(const Duration(seconds: 5));
      
      if (response.statusCode != 200) {
        developer.log('CheckHealth API Error: ${response.statusCode}', name: 'ApiService');
      }
      return response.statusCode == 200;
    } catch (e) {
      developer.log('CheckHealth API Exception: $e', name: 'ApiService', error: e);
      return false;
    }
  }
}

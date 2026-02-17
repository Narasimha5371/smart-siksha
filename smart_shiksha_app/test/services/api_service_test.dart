import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:smart_shiksha_app/services/api_service.dart';

void main() {
  group('ApiService', () {

    group('chat', () {
      test('returns answer when http call completes successfully', () async {
        final client = MockClient((request) async {
          if (request.url.toString() == '${ApiService.baseUrl}/chat') {
            return http.Response(jsonEncode({'answer': 'Hello AI'}), 200);
          }
          return http.Response('Not Found', 404);
        });

        final apiService = ApiService(client: client);
        final result = await apiService.chat('hello', 'en');

        expect(result, 'Hello AI');
      });

      test('returns "No response" when answer is null', () async {
        final client = MockClient((request) async {
          return http.Response(jsonEncode({}), 200);
        });

        final apiService = ApiService(client: client);
        final result = await apiService.chat('hello', 'en');

        expect(result, 'No response');
      });

      test('returns error message when http call returns error', () async {
        final client = MockClient((request) async {
          return http.Response('Internal Server Error', 500);
        });

        final apiService = ApiService(client: client);
        final result = await apiService.chat('hello', 'en');

        expect(result, 'Error: 500');
      });

      test('returns connection error message when http call throws exception', () async {
        final client = MockClient((request) async {
          throw Exception('Connection failed');
        });

        final apiService = ApiService(client: client);
        final result = await apiService.chat('hello', 'en');

        expect(result, 'Failed to connect to server. Please check your connection.');
      });

      test('sends correct request body', () async {
        final client = MockClient((request) async {
          final body = jsonDecode(request.body);
          expect(body['message'], 'test message');
          expect(body['language'], 'es');
          return http.Response(jsonEncode({'answer': 'Hola'}), 200);
        });

        final apiService = ApiService(client: client);
        await apiService.chat('test message', 'es');
      });
    });
  });
}

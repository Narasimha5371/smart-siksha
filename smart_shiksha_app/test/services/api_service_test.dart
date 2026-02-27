import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:smart_shiksha_app/services/api_service.dart';

class MockClient extends http.BaseClient {
  final Future<http.Response> Function(http.BaseRequest request) _handler;

  MockClient(this._handler);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final response = await _handler(request);
    return http.StreamedResponse(
      http.ByteStream.fromBytes(response.bodyBytes),
      response.statusCode,
      headers: response.headers,
      request: request,
    );
  }
}

void main() {
  group('ApiService Chat', () {
    test('returns answer when http call completes successfully', () async {
      final client = MockClient((request) async {
        return http.Response(jsonEncode({'answer': 'Hello, student!'}), 200);
      });

      final apiService = ApiService(client: client);
      final result = await apiService.chat('Hello', 'en');

      expect(result, 'Hello, student!');
    });

    test('returns error message when http call completes with error', () async {
      final client = MockClient((request) async {
        return http.Response('Internal Server Error', 500);
      });

      final apiService = ApiService(client: client);
      final result = await apiService.chat('Hello', 'en');

      expect(result, 'Error: 500');
    });

    test('returns connection error message when http call throws exception', () async {
      final client = MockClient((request) async {
        throw Exception('Network error');
      });

      final apiService = ApiService(client: client);
      final result = await apiService.chat('Hello', 'en');

      expect(result, 'Failed to connect to server. Please check your connection.');
    });
  });
}

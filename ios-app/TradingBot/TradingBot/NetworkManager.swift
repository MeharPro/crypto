import Foundation

class NetworkManager {
    static let shared = NetworkManager()
    private let baseURL = "http://127.0.0.1:5001"

    func startBot(parameters: [String: Any], completion: @escaping (Result<Void, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/start")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: [])
        } catch {
            completion(.failure(error))
            return
        }

        URLSession.shared.dataTask(with: request) { _, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            // Handle response...
            completion(.success(()))
        }.resume()
    }

    func stopBot(completion: @escaping (Result<Void, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/stop")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        URLSession.shared.dataTask(with: request) { _, _, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            completion(.success(()))
        }.resume()
    }

    func getStatus(completion: @escaping (Result<[String: Any], Error>) -> Void) {
        let url = URL(string: "\(baseURL)/status")!

        URLSession.shared.dataTask(with: url) { data, _, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                // Handle empty data...
                return
            }

            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                    completion(.success(json))
                }
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}

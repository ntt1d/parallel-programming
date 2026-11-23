#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;

class Matrix {
public:
    int n;
    vector<vector<double>> cells;
    explicit Matrix(int size) : n(size), cells(size, vector<double>(size, 0)) {}

    void load(ifstream& stream) {
        for (auto& row : cells)
            for (double& number : row)
                if (!(stream >> number)) throw runtime_error("Incorrect matrix data");
    }

    Matrix multiply(const Matrix& other) const {
        if (n != other.n) throw runtime_error("Matrix sizes do not match");
        Matrix answer(n);
        for (int j = 0; j < n; ++j)
            for (int i = 0; i < n; ++i) {
                double sum = 0;
                for (int k = 0; k < n; ++k)
                    sum += cells[i][k] * other.cells[k][j];
                answer.cells[i][j] = sum;
            }
        return answer;
    }

    void save(ofstream& stream) const {
        stream << n << '\n' << setprecision(17);
        for (const auto& row : cells) {
            for (double number : row) stream << number << ' ';
            stream << '\n';
        }
    }
};

int main() {
    try {
        ifstream first("A.txt"), second("B.txt");
        int n, m;
        if (!(first >> n) || !(second >> m) || n <= 0 || n != m)
            throw runtime_error("Cannot read matching matrix sizes");
        Matrix a(n), b(n);
        a.load(first);
        b.load(second);
        auto start = chrono::steady_clock::now();
        Matrix result = a.multiply(b);
        auto finish = chrono::steady_clock::now();
        ofstream output("result.txt");
        if (!output) throw runtime_error("Cannot open result.txt");
        result.save(output);
        double seconds = chrono::duration<double>(finish - start).count();
        long long size = n;
        cout << fixed << setprecision(6) << "time_sec=" << seconds
             << " N=" << n << " operations=" << 2LL * size * size * size
             << " memory_bytes=" << 3LL * size * size * sizeof(double) << '\n';
    } catch (const exception& error) {
        cerr << error.what() << '\n';
        return 1;
    }
}

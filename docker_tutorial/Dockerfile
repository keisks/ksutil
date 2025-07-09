# ベースイメージの指定（Python 3.10 の軽量イメージ）
FROM python:3.10-slim

# ビルド時の環境変数
ARG APP_DIR=/app

# ランタイム環境変数
ENV APP_NAME="SampleApp" \
    ENV_MODE="production"

# 作業ディレクトリの作成と移動
WORKDIR $APP_DIR

# wget, tar などの必要なツールをインストール（キャッシュは削除して最小化）
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget tar && \
    rm -rf /var/lib/apt/lists/*

# 例：外部からアーカイブを取得して明示的に解凍
RUN wget https://example.com/data/sample.tar.gz -O sample.tar.gz && \
    mkdir -p src && \
    tar -xzf sample.tar.gz -C src && \
    rm sample.tar.gz

# プロジェクトファイルのコピー
COPY . .

# パッケージのインストール（pipキャッシュも残さない）
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r src/requirements.txt

# ホストと共有するボリューム領域（ログなど）
VOLUME ["$APP_DIR/data"]

# ポート公開（例：FastAPI等）
EXPOSE 8000

# コンテナ起動時に常に実行されるコマンド
ENTRYPOINT ["python", "src/main.py"]

# デフォルト引数（docker run時に上書き可能）
CMD ["--mode=default"]


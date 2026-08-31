# MBAxMS Class Profile Directory — Project Proposal

## Overview

We propose to build a private web application that organizes the MBAxMS class profile in one accessible place. The website will display each classmate's profile photo, name, previous employment, desired industry, and LinkedIn profile link. The application will use Python and Django for the backend and will be deployed so that anyone with the shared class password can access it through a URL.

## Problem Statement

The MBAxMS cohort includes students with a wide variety of professional and national backgrounds. However, it can be difficult to remember everyone's experience and career interests or to identify classmates with relevant knowledge. This is especially true for us because we are only in the first week of the program and are still struggling to match each classmate's face with their name.

## Target Users

The primary users are students in the MBAxMS cohort. Because the application will contain personal information and profile photos, access will be limited to people who have the shared class password.

## Proposed Solution

The application will present classmates as a responsive collection of profile cards. Each card will include:

- Profile photo
- Name
- Previous employment
- Desired industry
- LinkedIn profile link

The first version will focus on making the class profile clear, attractive, and easy to browse on both desktop and mobile devices.

## Minimum Viable Product

The initial version will include:

1. A class profile page protected by a shared password. Anyone with the password can enter the site.
2. A card-based list of classmates.
3. A responsive layout for desktop and mobile screens.
4. A placeholder for profiles with no available photo.
5. Profile data loaded from a structured CSV file.

Search, filtering, individual profile pages, matching recommendations, and self-service profile editing may be considered as future improvements, but they are outside the scope of the initial version.

## Technical Approach

- **Backend:** Python with Django
- **Frontend:** HTML, CSS, and Bootstrap
- **Data processing:** Python's CSV tools or pandas
- **Data storage:** A structured CSV file and an application-managed image directory
- **Access control:** A shared class password stored securely as an environment variable; anyone with the password can access the site
- **Deployment:** A Python-compatible hosting platform that provides a shareable HTTPS URL

The profile dataset and photographs will not be stored in an unprotected public repository. The application will check authentication before returning profile information or image files.

## Data Structure

The profile CSV will use the following fields:

```text
id,name,photo_filename,previous_employment,desired_industry,linkedin_url
```

If a photograph or optional field is unavailable, the interface will show an appropriate placeholder rather than failing.

## Privacy and Consent

The application will contain personally identifiable information, so privacy is a core project requirement. Each classmate's information and photograph will be included only with their permission. The site will be password-protected, excluded from search-engine indexing, and shared only with the intended class community. Sensitive account information, private contact details, and any data not required for the stated purpose will not be collected.

## Development Milestones

1. Define the CSV format and prepare consented sample data.
2. Build the Python data-loading and validation logic.
3. Implement the password-protected profile page.
4. Create and refine the responsive profile-card design.
5. Test authentication, missing-data handling, and mobile display.
6. Deploy the application and verify access through its HTTPS URL.

## Deliverables

- A deployed class profile website with a Python backend
- Source code and setup instructions
- A short presentation or demonstration of the completed application

---

# MBAxMSクラスプロフィール・ディレクトリ — プロジェクト提案書

## 概要

MBAxMSクラスのプロフィールを一か所に整理する、クラス内限定のWebアプリケーションを開発します。Webサイトには、各クラスメイトの顔写真、名前、前職、希望業界、LinkedInのプロフィールリンクを掲載します。バックエンドにはPythonおよびdjangoを使用し、クラス共通パスワードを持っている人がURLからアクセスできる形でデプロイします。

## 課題

MBAxMSのクラスには、職業や国籍などの面で多様なバックグラウンドを持つ学生が集まっています。しかし、全員の経験やキャリアへの関心を覚えたり、関連する知識を持つクラスメイトを見つけたりすることは簡単ではありません。特にプログラムが始まって1週間目である我々は、それぞれの顔と名前を一致させることさえままなりません。

## 対象ユーザー

主なユーザーはMBAxMSコホートの学生です。個人情報と顔写真を扱うため、閲覧できるのはクラス共通パスワードを持っている人に限定します。

## 提案する解決策

クラスメイトをレスポンシブなプロフィールカードの一覧として表示します。各カードには、以下の情報を掲載します。

- 顔写真
- 名前
- 前職
- 希望業界
- LinkedInのプロフィールリンク

初期バージョンでは、デスクトップとモバイルの両方で、クラスプロフィールを分かりやすく、見やすく閲覧できることを重視します。

## MVP（初期バージョン）

初期バージョンには、以下の機能を含めます。

1. クラス共通パスワードで保護されたプロフィールページ（パスワードを持っている人は誰でもアクセス可能）
2. クラスメイトのカード形式の一覧表示
3. デスクトップとモバイルに対応したレスポンシブレイアウト
4. 顔写真がないプロフィールに使用するプレースホルダー
5. 構造化されたCSVファイルからのプロフィールデータ読み込み

検索、絞り込み、個別プロフィールページ、マッチング推薦、本人によるプロフィール編集は、将来の改善候補とします。これらは初期バージョンの対象外です。

## 技術的アプローチ

- **バックエンド:** PythonとDjango
- **フロントエンド:** HTML、CSS、Bootstrap
- **データ処理:** Python標準のCSV機能またはpandas
- **データ保存:** 構造化されたCSVファイルと、アプリケーションが管理する画像ディレクトリ
- **アクセス制御:** 環境変数として安全に保存するクラス共通パスワード（パスワードを持っている人は誰でもアクセス可能）
- **デプロイ:** HTTPSの共有URLを提供できるPython対応ホスティングサービス

プロフィールデータと写真は、保護されていない公開リポジトリには保存しません。アプリケーションは、プロフィール情報や画像ファイルを返す前に認証状態を確認します。

## データ構造

プロフィールCSVでは、以下の項目を使用します。

```text
id,name,photo_filename,previous_employment,desired_industry,linkedin_url
```
写真や任意項目がない場合はエラーにせず、適切なプレースホルダーを表示します。

## プライバシーと同意

本アプリケーションは個人を特定できる情報を扱うため、プライバシーをプロジェクトの中核要件とします。各クラスメイトの情報と写真は、本人の許可を得た場合にのみ掲載します。サイトはパスワードで保護し、検索エンジンのインデックス対象外に設定し、対象となるクラスコミュニティ内だけで共有します。アカウントに関する機密情報、非公開の連絡先、利用目的に不要なデータは収集しません。

## 開発マイルストーン

1. CSV形式を定義し、掲載許可を得たサンプルデータを準備する。
2. Pythonによるデータ読み込みと検証処理を実装する。
3. パスワードで保護されたプロフィールページを実装する。
4. レスポンシブなプロフィールカードのデザインを作成・改善する。
5. 認証、欠損データの処理、モバイル表示をテストする。
6. アプリケーションをデプロイし、HTTPS URLからアクセスできることを確認する。

## 成果物

- Pythonバックエンドを使用したデプロイ済みクラスプロフィールWebサイト
- ソースコードとセットアップ手順
- 完成したアプリケーションの短いプレゼンテーションまたはデモ

# MBAxMS Class Profile Directory — Project Proposal

## Overview

We propose to build a private web application that organizes the MBAxMS class profile in one accessible place. The website will help classmates learn one another's faces, names, backgrounds, and career interests. The application will use Python and Django for the backend and will be deployed at a shareable URL. Access will be limited through a combination of an approved CBS email address and a shared class access code based on the program's graduation date.

## Problem Statement

The MBAxMS cohort includes students with a wide variety of professional and national backgrounds. However, it can be difficult to remember everyone's experience and career interests or to identify classmates with relevant knowledge. This is especially true for us because we are only in the first week of the program and are still struggling to match each classmate's face with their name.

## Target Users

The primary users are students in the MBAxMS cohort. Because the application will contain personal information and profile photos, access will be limited to users whose CBS email addresses were collected and approved through the project’s Google Form and who also know the shared class access code (e.g., the expected graduation date).

## Proposed Solution

The application will present classmates as a responsive collection of profile cards. Each card will include:

- Profile photo
- Name
- Country or region of origin
- Previous employment
- Undergraduate institution
- Desired industry
- Hobbies
- Age, if the classmate chooses to provide it
- LinkedIn profile link

The first version will focus on making the class profile clear, attractive, and easy to browse on both desktop and mobile devices.

## Data Collection

Profile information will be collected through a Google Form. The form will request the profile fields listed above, a CBS email address, a profile-photo upload, and explicit consent to display the submitted information on the password-protected website.

Text responses will be stored in Google Sheets, while uploaded photographs will be stored in Google Drive. Before publication, the project team will review the responses and consent status. Approved records will then be imported into the Django application. Photographs will be resized and uploaded to private object storage rather than being stored in the public GitHub repository.

For the MVP, this import process will be performed manually after review. Automatic synchronization through Google APIs may be considered as a future enhancement.

## Minimum Viable Product

The initial version will include:

1. A login page requiring an approved CBS email address and the shared class access code.
2. An email allowlist created from approved Google Form responses.
3. A card-based list of classmates and their submitted profile information.
4. A responsive layout for desktop and mobile screens.
5. A placeholder for profiles with no available photo.
6. Profile data stored in PostgreSQL and private photographs stored in object storage.
7. A logout function and session-based access after successful login.

Search, filtering, individual profile pages, matching recommendations, self-service profile editing, and full CBS or Google single sign-on may be considered as future improvements, but they are outside the scope of the initial version.

## Access Control

At login, the application will normalize the submitted email address by trimming spaces and converting it to lowercase. Access will be granted only when the email matches an active address in the approved allowlist and the submitted class access code matches the value stored securely in the deployment environment.

The class access code will be based on the program's graduation date, but the actual value will never be stored in GitHub, the database, the proposal, or the profile CSV. The login page will return the same generic error message whether the email or access code is incorrect. Repeated failed login attempts will be rate-limited. After successful login, Django will issue a secure session cookie.

This MVP mechanism is an access-control measure rather than full email ownership verification: entering an allowlisted email does not prove that the person currently controls that mailbox. A future production version should replace it with verified CBS or Google sign-in.

## Technical Approach

- **Data collection:** Google Forms, Google Sheets, and Google Drive
- **Backend:** Python with Django
- **Frontend:** Django templates, HTML, CSS, and Bootstrap
- **Application hosting:** Render Free web service
- **Database:** Render Free PostgreSQL
- **Photo storage:** Private Cloudflare R2 bucket
- **Access control:** Approved CBS email allowlist plus a shared class access code stored as a Render environment variable
- **Deployment:** A Render HTTPS URL connected to the GitHub repository

The project will use free tiers because the MVP and demonstration period will be completed within 30 days. The free Render web service may require a short startup period after inactivity, and the free PostgreSQL database expires after 30 days. Long-term operation would therefore require migration to a persistent paid database or another long-term hosting arrangement.

The profile dataset, email allowlist, access code, and photographs will not be stored in the public GitHub repository. Django will verify the session before returning profile information or photographs.

## Data Structure

The primary profile record will include:

```text
id
full_name
cbs_email
photo_storage_key
country_of_origin
previous_employment
undergraduate_institution
desired_industry
hobbies
age
linkedin_url
consent_confirmed_at
```

The CBS email address will be used for the login allowlist and will not be displayed on the public-facing profile card. Age and other optional fields will be omitted from the card when not provided. If a photograph is unavailable, the interface will display an appropriate placeholder rather than failing.

## Privacy and Consent

The application will contain personally identifiable information, so privacy is a core project requirement. Each classmate's information and photograph will be included only with their explicit permission. Optional information, including age, may be left blank. The site will be access-controlled, excluded from search-engine indexing, and shared only with the intended class community.

The team will not collect dates of birth, private contact information, account passwords, or information unnecessary for the project. A classmate may request that their profile be corrected or removed. In that case, the corresponding record will be deactivated and its photograph removed from application storage.

## Development Milestones

1. Finalize the Google Form, profile fields, photo requirements, and consent language.
2. Collect and review sample responses, then prepare the approved email allowlist.
3. Build the Django profile model and the Google Forms data-import process.
4. Implement the email-and-access-code login flow and secure sessions.
5. Build and refine the responsive profile-card interface.
6. Configure PostgreSQL and private photo storage.
7. Deploy the application on Render's free tier.
8. Test authentication, unauthorized access, missing data, photo privacy, and mobile display.

## Deliverables

- A deployed class profile website with a Python and Django backend
- A Google Form for collecting profile data, photographs, and consent
- Source code and setup instructions
- A short presentation or demonstration of the completed application

---

# MBAxMSクラスプロフィール・ディレクトリ — プロジェクト提案書

## 概要

MBAxMSクラスのプロフィールを一か所に整理する、クラス内限定のWebアプリケーションを開発します。このWebサイトにより、クラスメイト同士がそれぞれの顔、名前、バックグラウンド、キャリアへの関心を把握しやすくします。バックエンドにはPythonおよびDjangoを使用し、共有可能なURLへデプロイします。Googleフォームで収集・承認されたCBSメールアドレスと、プログラムの卒業年月日に基づくクラス共通アクセスコードを組み合わせてアクセスを制限します。

## 課題

MBAxMSのクラスには、職業や国籍などの面で多様なバックグラウンドを持つ学生が集まっています。しかし、全員の経験やキャリアへの関心を覚えたり、関連する知識を持つクラスメイトを見つけたりすることは簡単ではありません。特にプログラムが始まって1週間目である我々は、それぞれの顔と名前を一致させることさえままなりません。

## 対象ユーザー

主なユーザーはMBAxMSコホートの学生です。個人情報と顔写真を扱うため、Googleフォームを通じて収集・承認されたCBSメールアドレスを入力し、かつクラス共通アクセスコード（ex. 卒業予定日など）を知っている人だけが閲覧できます。

## 提案する解決策

クラスメイトをレスポンシブなプロフィールカードの一覧として表示します。各カードには、以下の情報を掲載します。

- 顔写真
- 名前
- 出身国または地域
- 前職
- 出身大学
- 希望業界
- 趣味
- 本人が掲載を希望する場合の年齢
- LinkedInのプロフィールリンク

初期バージョンでは、デスクトップとモバイルの両方で、クラスプロフィールを分かりやすく、見やすく閲覧できることを重視します。

## データ収集

プロフィール情報はGoogleフォームで収集します。フォームでは、上記のプロフィール項目、CBSメールアドレス、顔写真のアップロード、およびパスワードで保護されたWebサイトに情報を掲載することへの明示的な同意を求めます。

テキスト回答はGoogle Sheetsに、アップロードされた写真はGoogle Driveに保存されます。公開前に、プロジェクトチームが回答内容と同意状況を確認します。承認されたレコードだけをDjangoアプリケーションへ取り込みます。写真はサイズを調整して非公開のオブジェクトストレージへアップロードし、公開GitHubリポジトリには保存しません。

MVPでは、確認後の取り込みを手動で行います。Google APIを使った自動同期は将来の改善候補とします。

## MVP（初期バージョン）

初期バージョンには、以下の機能を含めます。

1. 承認済みCBSメールアドレスとクラス共通アクセスコードを入力するログインページ
2. 承認済みGoogleフォーム回答から作成するメールアドレスのallowlist
3. クラスメイトと提出済みプロフィール情報のカード形式の一覧表示
4. デスクトップとモバイルに対応したレスポンシブレイアウト
5. 顔写真がないプロフィールに使用するプレースホルダー
6. PostgreSQLに保存するプロフィール情報と、オブジェクトストレージに非公開で保存する写真
7. ログアウト機能と、ログイン成功後のセッションによるアクセス維持

検索、絞り込み、個別プロフィールページ、マッチング推薦、本人によるプロフィール編集、正式なCBSまたはGoogleシングルサインオンは、将来の改善候補とします。これらは初期バージョンの対象外です。

## アクセス制御

ログイン時に、入力されたメールアドレスの前後の空白を削除し、小文字に統一します。メールアドレスが承認済みallowlistの有効なアドレスと一致し、かつ入力されたクラス共通アクセスコードがデプロイ環境に安全に保存された値と一致する場合にのみアクセスを許可します。

クラス共通アクセスコードにはプログラムの卒業年月日を使用しますが、実際の値はGitHub、データベース、提案書、プロフィールCSVのいずれにも保存しません。メールアドレスとアクセスコードのどちらが間違っていても、ログイン画面には同じ一般的なエラーメッセージを表示します。連続するログイン失敗には回数制限を設けます。ログインに成功すると、Djangoが安全なセッションCookieを発行します。

このMVP方式は完全なメール所有者確認ではなく、アクセス制限です。allowlistに登録されたメールアドレスを入力しても、その人が現在そのメールボックスを所有していることまでは証明できません。正式運用する場合は、確認済みのCBSまたはGoogleログインに置き換えます。

## 技術的アプローチ

- **データ収集:** Google Forms、Google Sheets、Google Drive
- **バックエンド:** PythonとDjango
- **フロントエンド:** Djangoテンプレート、HTML、CSS、Bootstrap
- **アプリケーションホスティング:** Renderの無料Webサービス
- **データベース:** Renderの無料PostgreSQL
- **写真保存:** Cloudflare R2の非公開bucket
- **アクセス制御:** 承認済みCBSメールallowlistと、Renderの環境変数に保存するクラス共通アクセスコード
- **デプロイ:** GitHubリポジトリと接続したRenderのHTTPS URL

MVPとデモを30日以内に完了するため、各サービスの無料枠を利用します。Renderの無料Webサービスは、一定時間アクセスがない場合、次回アクセス時の起動に時間がかかる可能性があります。また、無料PostgreSQLは30日後に失効します。そのため、長期運用する場合は、永続的な有料データベースまたは別の長期ホスティング環境へ移行する必要があります。

プロフィールデータ、メールallowlist、アクセスコード、顔写真は、公開GitHubリポジトリには保存しません。Djangoはプロフィール情報や写真を返す前にセッションを確認します。

## データ構造

主要なプロフィールレコードには、以下の項目を保存します。

```text
id
full_name
cbs_email
photo_storage_key
country_of_origin
previous_employment
undergraduate_institution
desired_industry
hobbies
age
linkedin_url
consent_confirmed_at
```

CBSメールアドレスはログインallowlistに使用し、プロフィールカードには表示しません。年齢などの任意項目は、回答がない場合にはカード上に表示しません。写真がない場合はエラーにせず、適切なプレースホルダーを表示します。

## プライバシーと同意

本アプリケーションは個人を特定できる情報を扱うため、プライバシーをプロジェクトの中核要件とします。各クラスメイトの情報と写真は、本人の明示的な許可を得た場合にのみ掲載します。年齢を含む任意情報は、未回答でも構いません。サイトはアクセス制限を設け、検索エンジンのインデックス対象外に設定し、対象となるクラスコミュニティ内だけで共有します。

生年月日、非公開の連絡先、アカウントのパスワード、利用目的に不要な情報は収集しません。クラスメイトは、自分のプロフィールの修正または削除を依頼できます。その場合、該当レコードを無効化し、写真をアプリケーションのストレージから削除します。

## 開発マイルストーン

1. Googleフォーム、プロフィール項目、写真要件、同意文を確定する。
2. サンプル回答を収集・確認し、承認済みメールallowlistを準備する。
3. DjangoのプロフィールモデルとGoogleフォーム回答の取り込み処理を構築する。
4. メールアドレスとアクセスコードによるログイン、および安全なセッションを実装する。
5. レスポンシブなプロフィールカード画面を作成・改善する。
6. PostgreSQLと非公開写真ストレージを設定する。
7. Renderの無料枠へアプリケーションをデプロイする。
8. 認証、未認証アクセス、欠損データ、写真の非公開性、モバイル表示をテストする。

## 成果物

- PythonとDjangoをバックエンドに使用したデプロイ済みクラスプロフィールWebサイト
- プロフィール情報、写真、同意を収集するGoogleフォーム
- ソースコードとセットアップ手順
- 完成したアプリケーションの短いプレゼンテーションまたはデモ

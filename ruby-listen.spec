#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	listen
Summary:	Listen to file modifications
Name:		ruby-%{pkgname}
Version:	0.4.7
Release:	0.2
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	068e217a5d4e28690370c4f8eaa2b73e
# git clone https://github.com/guard/listen.git && cd listen
# git checkout v0.4.7
# tar czvf listen-0.4.7-specs.tar.gz spec/
Source1:	listen-%{version}-specs.tar.gz
Patch0:		deps.patch
URL:		https://github.com/guard/listen
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
BuildRequires:	ruby-bundler
BuildRequires:	ruby-rspec
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Listen gem listens to file modifications and notifies you about
the changes. Works everywhere!

%prep
%setup -q -n %{pkgname}-%{version} -a1

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
rspec spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

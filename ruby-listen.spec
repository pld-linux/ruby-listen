#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	listen
Summary:	Listen to file modifications
Name:		ruby-%{pkgname}
Version:	3.10.0
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	https://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	3f567f78d0328b7a9148e95497b1f30f
URL:		https://github.com/guard/listen
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
%if %{with tests}
BuildRequires:	ruby-rspec >= 3
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Listen gem listens to file modifications and notifies you about
the changes. Works everywhere!

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE.txt
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
